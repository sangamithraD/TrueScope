// firebaseConfig.js
import { initializeApp } from "firebase/app";
import { initializeAuth, getReactNativePersistence } from "firebase/auth";
import ReactNativeAsyncStorage from "@react-native-async-storage/async-storage";

const firebaseConfig = {
  apiKey: "AIzaSyCFbNqvMw606wAtC8ZxylScrsTt9jlunmw",
  authDomain: "truthmap123.firebaseapp.com",
  projectId: "truthmap123",
  storageBucket: "truthmap123.firebasestorage.app",
  messagingSenderId: "291957944201",
  appId: "1:291957944201:web:50d2e055d1d1429bb83b58",
  measurementId: "G-9YFZMGWJJ6",
};

const app = initializeApp(firebaseConfig);

// ✅ Fix for Expo Go: use AsyncStorage for persistence
export const auth = initializeAuth(app, {
  persistence: getReactNativePersistence(ReactNativeAsyncStorage),
});
