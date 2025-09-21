import React, { useState, useEffect } from "react";
import { View, StyleSheet, Dimensions, Text, TouchableOpacity } from 'react-native';
import MapView, { Polygon } from "react-native-maps";
import { Searchbar } from "react-native-paper";
const indiaStates = require('../assets/india_state.json');

import axios from "axios";

export default function MapScreen() {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedState, setSelectedState] = useState(null);
  const [fakeNewsList, setFakeNewsList] = useState([]);
  const [stateLevels, setStateLevels] = useState({}); // backend data

  // Fetch fake news levels for each state from backend
  useEffect(() => {
    axios.get("http://YOUR_BACKEND_API/states").then((res) => {
      // Example response: { "Tamil Nadu": "high", "Kerala": "medium" }
      setStateLevels(res.data);
    });
  }, []);

  const getColor = (stateName) => {
    const level = stateLevels[stateName];
    if (level === "high") return "rgba(245, 40, 40, 0.67)";   // red
    if (level === "medium") return "rgba(216, 231, 5, 0.91)"; // yellow
    if (level === "low") return "rgba(0,255,0,0.5)";    // green
    return "rgba(200,200,200,0.3)"; // default grey
  };

  const handleStatePress = (stateName) => {
    setSelectedState(stateName);
    axios.get(`http://YOUR_BACKEND_API/fakenews/${stateName}`).then((res) => {
      setFakeNewsList(res.data);
    });
  };

  return (
    <View style={styles.container}>
      {/* Search Bar */}
      <Searchbar
        placeholder="Check news..."
        onChangeText={(q) => setSearchQuery(q)}
        value={searchQuery}
        style={styles.searchBar}
      />

    <MapView
  style={styles.map}
  initialRegion={{
    latitude: 22.9734,
    longitude: 78.6569,
    latitudeDelta: 20,
    longitudeDelta: 20,
  }}
>
  {indiaStates.features
    .filter(feature =>
      feature.properties.st_nm.toLowerCase().includes(searchQuery.toLowerCase())
    )
    .map((feature, index) => {
      const stateName = feature.properties.st_nm;
      const coordinates = feature.geometry.coordinates[0].map(([lng, lat]) => ({
        latitude: lat,
        longitude: lng,
      }));

      return (
        <Polygon
          key={index}
          coordinates={coordinates}
          fillColor={
            selectedState === stateName
              ? 'rgba(255,0,0,0.5)' // highlight selected state
              : getColor(stateName)
          }
          strokeColor="black"
          strokeWidth={1}
          tappable={true}
          onPress={() => handleStatePress(stateName)}
        />
      );
    })}
</MapView>


      {/* Fake News List */}
      {selectedState && (
        <View style={styles.listContainer}>
          <Text style={styles.listTitle}>
            Trending Fake News in {selectedState}
          </Text>
          <FlatList
            data={fakeNewsList}
            keyExtractor={(item, index) => index.toString()}
            renderItem={({ item }) => (
              <Text style={styles.newsItem}>• {item}</Text>
            )}
          />
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  map: { flex: 1 },
  searchBar: {
    position: "absolute",
    top: 40,
    left: 10,
    right: 10,
    zIndex: 1,
  },
  listContainer: {
    position: "absolute",
    bottom: 0,
    left: 0,
    right: 0,
    maxHeight: "40%",
    backgroundColor: "white",
    padding: 10,
    borderTopLeftRadius: 12,
    borderTopRightRadius: 12,
  },
  listTitle: { fontSize: 16, fontWeight: "bold", marginBottom: 5 },
  newsItem: { fontSize: 14, marginBottom: 3 },
});
