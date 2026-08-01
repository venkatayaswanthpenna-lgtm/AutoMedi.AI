import { initializeApp, getApps } from "firebase/app";
import { getAnalytics, isSupported } from "firebase/analytics";

const firebaseConfig = {
  apiKey: "AIzaSyD06ZYGmhh5WiJrje17PeQY3fykgkX6pSI",
  authDomain: "automedi-ai.firebaseapp.com",
  projectId: "automedi-ai",
  storageBucket: "automedi-ai.firebasestorage.app",
  messagingSenderId: "1087181523415",
  appId: "1:1087181523415:web:70acce3707de2197ac2392",
  measurementId: "G-CN8KDYT118"
};

// Initialize Firebase only if it hasn't been initialized already (useful for Next.js hot reloading)
const app = getApps().length === 0 ? initializeApp(firebaseConfig) : getApps()[0];

// Initialize Analytics conditionally (only runs in the browser)
let analytics: any = null;
if (typeof window !== "undefined") {
  isSupported().then((yes) => {
    if (yes) {
      analytics = getAnalytics(app);
    }
  });
}

export { app, analytics };
