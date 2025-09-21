import React, { useState, useEffect, useRef } from "react";
import {
  View,
  Text,
  TextInput,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  Animated,
  Dimensions,
} from "react-native";
import MapView, { Polygon } from "react-native-maps";

const { height } = Dimensions.get("window");

// Mock fake news levels
const mockStateLevels = {
  "Tamil Nadu": "high",
  "Kerala": "medium",
  "Karnataka": "low",
  "Andaman and Nicobar": "medium",
  "Maharashtra": "high",
};

// Mock fake news per state
const mockFakeNews = {
  "Tamil Nadu": ["Fake news 1 TN", "Fake news 2 TN"],
  "Kerala": ["Fake news 1 KL", "Fake news 2 KL"],
  "Karnataka": ["Fake news 1 KA"],
  "Andaman and Nicobar": ["Fake news 1 AN"],
};

const indiaStates = require("../assets/india_state.json");

export default function NewsScreen() {
  const [newsText, setNewsText] = useState("");
  const [selectedState, setSelectedState] = useState(null);
  const [fakeNewsList, setFakeNewsList] = useState([]);
  const [colors, setColors] = useState({});
  const [popupMessage, setPopupMessage] = useState("");
  const popupAnim = useRef(new Animated.Value(height)).current;

  // --- Initialize colors immediately ---
  useEffect(() => {
    const initialColors = {};
    indiaStates.features.forEach((f) => {
      const name = f.properties.NAME_1;
      const level = mockStateLevels[name];
      if (level === "high") initialColors[name] = "rgba(245,40,40,0.7)";
      else if (level === "medium") initialColors[name] = "rgba(216,231,5,0.7)";
      else if (level === "low") initialColors[name] = "rgba(0,255,0,0.5)";
      else initialColors[name] = "rgba(200,200,200,0.3)";
    });
    setColors(initialColors);
  }, []);

  // --- Show bottom popup smoothly ---
  const showPopup = (message) => {
    setPopupMessage(message);
    Animated.timing(popupAnim, {
      toValue: 0,
      duration: 300,
      useNativeDriver: true,
    }).start();

    setTimeout(() => {
      Animated.timing(popupAnim, {
        toValue: height,
        duration: 300,
        useNativeDriver: true,
      }).start();
    }, 3000);
  };

  const handleStatePress = (stateName) => {
    setSelectedState(stateName);
    setFakeNewsList(mockFakeNews[stateName] || []);

    const level = mockStateLevels[stateName] || "unknown";
    showPopup(`Fake news spreading level is ${level.toUpperCase()} in ${stateName}`);
  };

  const checkNews = () => {
    if (!newsText) return;
    if (newsText.toLowerCase().includes("not")) {
      showPopup("⚠️ This is FAKE news!");
    } else {
      showPopup("✅ This is REAL news!");
    }
  };

  return (
    <View style={styles.container}>
      {/* Legend */}
      <View style={styles.legendContainer}>
        <View style={styles.legendItem}>
          <View style={[styles.colorBox, { backgroundColor: "rgba(245,40,40,0.7)" }]} />
          <Text style={styles.legendText}>High</Text>
        </View>
        <View style={styles.legendItem}>
          <View style={[styles.colorBox, { backgroundColor: "rgba(216,231,5,0.7)" }]} />
          <Text style={styles.legendText}>Medium</Text>
        </View>
        <View style={styles.legendItem}>
          <View style={[styles.colorBox, { backgroundColor: "rgba(0,255,0,0.5)" }]} />
          <Text style={styles.legendText}>Low</Text>
        </View>
      </View>

      {/* Check News Box */}
      <TextInput
        style={styles.input}
        placeholder="Paste news here..."
        placeholderTextColor="#94A3B8"
        value={newsText}
        onChangeText={setNewsText}
      />
      <TouchableOpacity style={styles.button} onPress={checkNews}>
        <Text style={styles.buttonText}>Submit</Text>
      </TouchableOpacity>

      {/* Map */}
      <MapView
        style={styles.map}
        initialRegion={{
          latitude: 20.5937,
          longitude: 78.9629,
          latitudeDelta: 20,
          longitudeDelta: 20,
        }}
      >
        {indiaStates.features.map((feature, index) => {
          const stateName = feature?.properties?.NAME_1 || "Unknown";
          const geometry = feature.geometry;
          if (!geometry) return null;
          const polygons = geometry.type === "Polygon" ? [geometry.coordinates] : geometry.coordinates;

          return polygons.map((poly, i) => {
            const coords = poly[0].map(([lng, lat]) => ({ latitude: lat, longitude: lng }));
            return (
              <Polygon
                key={`${index}-${i}`}
                coordinates={coords}
                strokeColor="black"
                fillColor={selectedState === stateName ? "rgba(255,0,0,0.5)" : colors[stateName]}
                strokeWidth={1}
                tappable
                onPress={() => handleStatePress(stateName)}
              />
            );
          });
        })}
      </MapView>

      {/* Trending Fake News List */}
      {selectedState && (
        <View style={styles.listContainer}>
          <Text style={styles.listTitle}>Trending Fake News in {selectedState}</Text>
          <FlatList
            data={fakeNewsList}
            keyExtractor={(item, idx) => idx.toString()}
            renderItem={({ item }) => <Text style={styles.newsItem}>• {item}</Text>}
          />
        </View>
      )}

      {/* Bottom Popup */}
      <Animated.View
        style={[
          styles.popup,
          {
            transform: [{ translateY: popupAnim }],
          },
        ]}
      >
        <Text style={styles.popupText}>{popupMessage}</Text>
      </Animated.View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#0F172A", padding: 10 },
  legendContainer: {
    flexDirection: "row",
    justifyContent: "space-around",
    marginBottom: 10,
    padding: 5,
    backgroundColor: "#1E293B",
    borderRadius: 10,
  },
  legendItem: { flexDirection: "row", alignItems: "center" },
  colorBox: { width: 20, height: 20, marginRight: 5, borderRadius: 4 },
  legendText: { color: "#fff", fontWeight: "bold" },
  input: {
    width: "100%",
    backgroundColor: "#1E293B",
    padding: 12,
    borderRadius: 10,
    marginBottom: 10,
    color: "#F8FAFC",
  },
  button: {
    backgroundColor: "#2563EB",
    padding: 12,
    borderRadius: 8,
    marginBottom: 10,
    alignItems: "center",
  },
  buttonText: { color: "#fff", fontWeight: "bold", fontSize: 16 },
  map: { width: "100%", flex: 1, marginBottom: 10 },
  listContainer: {
    maxHeight: 200,
    backgroundColor: "#fff",
    padding: 10,
    marginTop: 10,
    borderRadius: 10,
  },
  listTitle: { fontWeight: "bold", marginBottom: 5 },
  newsItem: { fontSize: 14, marginBottom: 3 },
  popup: {
    position: "absolute",
    left: 20,
    right: 20,
    bottom: 20,
    backgroundColor: "rgba(0,0,0,0.85)",
    padding: 15,
    borderRadius: 10,
  },
  popupText: { color: "#fff", fontWeight: "bold", textAlign: "center" },
});
