import {useState} from 'react';
import { send_csv } from '../services/api';
import { Button } from "@chakra-ui/react"

export default function UploadCSV({statsChanger}){

    const [file, setFile] = useState(null);
    
    const onFileChange = (event) => {
        setFile(event.target.files[0]);
    }

    const onFileUpload = async () => {
        const formData = new FormData();
        formData.append('csv_file', file);
        const res = await send_csv(formData);
        statsChanger(res);
        console.log(res);
    }

    return (
        <div>
            <h1>Upload your Letterboxd watched.csv file</h1>
            <input type="file" accept=".csv" id='selectedFile' style={{display: 'none'}} onChange={onFileChange}/>
            <input type="button" value="Choose File" onClick={() => document.getElementById('selectedFile').click()} />
            { file && (
                <div>
                    <h2>File Selected: {file.name}</h2>
                    <Button onClick={onFileUpload}>Get Your Stats!</Button>
                </div>
            )}
        </div>
    )
}