import React, { Component, useEffect, useRef } from "react";
import { useState } from "react";
import RecognizedSubjects from "./RecognizedSubjects";

const HomePage = () => {
    const formData = useRef(new FormData());
    const [studentData, setStudentData] = useState(null);
    const [majorsData, setMajorsData] = useState(null);
    const [currentStudentMajor, setCurrentStudentMajor] = useState(null);
    const [futureStudentMajor, setFutureStudentMajor] = useState(null);
    const [currentStudentMajorId, setCurrentStudentMajorId] = useState(null);
    const [futureStudentMajorId, setFutureStudentMajorId] = useState(null);
    const [fileName, setFileName] = useState("");
    const [transferId, setTransferId] = useState("");
    const [requiredStudentSubjects, setRequiredStudentSubjects] =
        useState(null);
    const [recognizedStudentSubjects, setRecognizedStudentSubjects] =
        useState(null);
    const [error, setError] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    useEffect(() => {
        fetchMajors();
    }, []);

    const fetchMajors = async () => {
        try {
            const response = await fetch(`http://127.0.0.1:8000/api/get-data`);
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            const res = await response.json();
            await setMajorsData(res); // Assuming the API returns JSON
        } catch (error) {
            setError(error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleCurrentMajorSelect = async (event) => {
        setCurrentStudentMajorId(event.target.value);
        setCurrentStudentMajor(await getSubjects(event.target.value));
        console.log("Current student major: ", event.target.value);
    };

    const handleFutureMajorSelect = async (event) => {
        setFutureStudentMajorId(event.target.value);
        setFutureStudentMajor(await getSubjects(event.target.value));
        console.log("Future student major: ", event.target.value);
    };

    const handleFileUpload = (event) => {
        const file = event.target.files[0];
        setFileName(file.name);
        formData.current.append("file", file);
    };

    const handleFileUploadClick = async () => {
        setStudentData(null);
        setRecognizedStudentSubjects(null);
        setRequiredStudentSubjects(null);
        setIsLoading(true);
        if (!currentStudentMajor || !futureStudentMajor) {
            console.log("Current student major: ", currentStudentMajor);
            console.log("Future student major: ", futureStudentMajor);
            alert("Not enough data.");
            setIsLoading(false);
            return;
        }

        setTransferId(currentStudentMajorId + "-" + futureStudentMajorId);

        await fetch("http://127.0.0.1:8000/api/extract", {
            // Your POST endpoint
            method: "POST",
            body: formData.current, // This is your file object
        })
            .then(
                (response) => response.json() // if the response is a JSON object
            )
            .then(
                (success) => {
                    success.student_current_major = currentStudentMajor;
                    success.student_future_major = futureStudentMajor;
                    setStudentData(success);
                    console.log("The data of the student: ", success);
                    console.log(
                        "OCR Recognized subjects: ",
                        success.student_grades
                    );
                    deletePdfFile();
                    setIsLoading(false);
                } // Handle the success response object
            )
            .catch(
                (error) => console.log(error) // Handle the error response object
            );
    };

    const deletePdfFile = () => {
        fetch("http://127.0.0.1:8000/api/delete-pdf-file", {
            method: "GET",
        })
            .then(
                (response) => response.json() // if the response is a JSON object
            )
            .then(
                (success) => {
                    console.log(success);
                    setIsLoading(false);
                } // Handle the success response object
            )
            .catch(
                (error) => console.log(error) // Handle the error response object
            );
    };

    const getSubjects = async (major) => {
        let subjects;

        await fetch("http://127.0.0.1:8000/api/get-major-data", {
            method: "POST",
            body: major,
        })
            .then(
                (response) => response.json() // if the response is a JSON object
            )
            .then(
                (success) => {
                    subjects = success;
                    console.log("Subjects of the major: ", success);
                    setIsLoading(false);
                } // Handle the success response object
            )
            .catch(
                (error) => console.log(error) // Handle the error response object
            );

        return subjects;
    };

    return (
        <div className="HomePage">
            <div className="home-page-content">
                <h1>Prebacivanje smjerova</h1>

                <div className="select-majors">
                    <div className="current-major-select">
                        <label htmlFor="current-major">
                            Studentov trenutni smjer:
                        </label>

                        <select
                            name="current-major"
                            id="current-major-select"
                            onChange={() => handleCurrentMajorSelect(event)}
                        >
                            <option value=""></option>
                            {majorsData &&
                                majorsData.map((currentMajor) => (
                                    <option
                                        key={currentMajor.id}
                                        value={currentMajor.id}
                                    >
                                        {currentMajor.name}
                                    </option>
                                ))}
                        </select>
                    </div>

                    <div className="future-major-select">
                        <label htmlFor="future-major">
                            Smjer na koji se student prebacuje:
                        </label>

                        <select
                            name="future-major"
                            id="future-major-select"
                            onChange={() => handleFutureMajorSelect(event)}
                        >
                            <option value=""></option>
                            {majorsData &&
                                majorsData.map((futureMajor) => (
                                    <option
                                        key={futureMajor.id}
                                        value={futureMajor.id}
                                    >
                                        {futureMajor.name}
                                    </option>
                                ))}
                        </select>
                    </div>
                </div>

                <div className="file-upload-div">
                    <p></p>
                    <label htmlFor="file-upload" className="custom-file-upload">
                        Browse
                    </label>
                    <input
                        type="file"
                        id="file-upload"
                        onChange={() => handleFileUpload(event)}
                    />
                    <p>{fileName}</p>
                    <button onClick={handleFileUploadClick}>Confirm</button>
                </div>

                {isLoading && <p className="loading">Loading...</p>}
                {studentData && (
                    <div className="student-info">
                        <h2 className="student-name">
                            Student: {studentData.student_name}
                        </h2>

                        {studentData && (
                            <RecognizedSubjects
                                student={studentData}
                                transfer={
                                    currentStudentMajorId +
                                    "-" +
                                    futureStudentMajorId
                                }
                                requiredStudentSubjects={
                                    requiredStudentSubjects
                                }
                                setRequiredStudentSubjects={
                                    setRequiredStudentSubjects
                                }
                                recognizedStudentSubjects={
                                    recognizedStudentSubjects
                                }
                                setRecognizedStudentSubjects={
                                    setRecognizedStudentSubjects
                                }
                                currentStudentMajor={currentStudentMajor}
                                futureStudentMajor={futureStudentMajor}
                                isLoading={isLoading}
                                setIsLoading={setIsLoading}
                            />
                        )}
                    </div>
                )}
            </div>
        </div>
    );
};

export default HomePage;
