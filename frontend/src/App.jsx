import { useCallback, useEffect, useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";

function App() {
    const [images, setImages] = useState([]);
    const [selectedImage, setSelectedImage] = useState({});

    const fetchImages = useCallback(() => {}, []);

    useEffect(() => {
        fetchImages();
    }, []);

    return (
        <div>
            <div></div>
            <div></div>
        </div>
    );
}

export default App;
