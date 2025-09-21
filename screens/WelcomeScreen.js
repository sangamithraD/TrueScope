import React from "react";
import { View, Text, StyleSheet, TouchableOpacity } from "react-native";
import { LinearGradient } from "expo-linear-gradient";

export default function WelcomeScreen({ navigation }) {
  return (
    <LinearGradient
      colors={["#f30b96f0", "#0c92ebff", "#d6c911ff"]}
      style={styles.container}
    >
      {/* Removed emoji/logo */}

      <Text style={styles.title}>Welcome to</Text>
      <Text style={styles.brand}>TrueScope</Text>

      <Text style={styles.subtitle}>
        💡Spot fake.                          
        
        Stay smart{"\n"}
        
      </Text>

      <TouchableOpacity
        style={styles.button}
        onPress={() => navigation.navigate("Login")}
      >
        <Text style={styles.buttonText}>⚡ Get Started</Text>
      </TouchableOpacity>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    padding: 20,
  },
  title: {
    fontSize: 26,
    color: "#E2E8F0",
    fontWeight: "600",
  },
  brand: {
    fontSize: 48,
    color: "#14f80cff",
    fontWeight: "900",
    marginVertical: 10,
    textShadowColor: "#060606ff",
    textShadowOffset: { width: 2, height: 2 },
    textShadowRadius: 12,
  },
  subtitle: {
    fontSize: 16,
    color: "#010103ff",
    textAlign: "center",
    marginBottom: 40,
  },
  button: {
    backgroundColor: "#d1dc2cff",
    paddingVertical: 14,
    paddingHorizontal: 50,
    borderRadius: 50,
    elevation: 8,
  },
  buttonText: {
    color: "#fff",
    fontSize: 18,
    fontWeight: "800",
    textShadowColor: "#000",
    textShadowOffset: { width: 1, height: 1 },
    textShadowRadius: 3,
  },
});
