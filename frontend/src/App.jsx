import { useCallback, useEffect, useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";
import axios from "axios";

function App() {
    const COLS = 10;

    const [imageSet, setImageSet] = useState([]);
    const [selectedImage, setSelectedImage] = useState({});

    const fetchImages = useCallback(async () => {
        const response = await axios.get("http://localhost:8000/images");
        const imageDataset = [];
        if (response.status === 200) {
            let imageData = response.data;
            while (imageData.length) {
                imageDataset.push(imageData.splice(0, COLS));
            }
            setImageSet(imageDataset);
        }
    }, []);

    console.log(selectedImage);

    useEffect(() => {
        fetchImages();
    }, []);

    return (
        <div>
            <div>
                <button>추론</button>
            </div>
            <div className="">
                <table>
                    {imageSet.map((images) => {
                        return (
                            <tr>
                                {images.map((image) => (
                                    <td>
                                        <img
                                            onClick={(event) =>
                                                setSelectedImage(image)
                                            }
                                            id={image.fileName}
                                            alt={image.fileName}
                                            src={`data:image/png;base64, ${image.base64}`}
                                        />
                                    </td>
                                ))}
                            </tr>
                        );
                    })}
                </table>
            </div>
        </div>
    );
}

export default App;
