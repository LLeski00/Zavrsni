import React, { Component, useEffect } from "react";
import { useState } from "react";

const HomePage = () => {
    let file;
    let formData = new FormData();
    const [studentData, setStudentData] = useState(null);
    const [majorsData, setMajorsData] = useState(null);
    const [currentStudentMajor, setCurrentStudentMajor] = useState(null);
    const [futureStudentMajor, setFutureStudentMajor] = useState(null);
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
            console.log(res);
        } catch (error) {
            setError(error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleCurrentMajorSelect = async (event) => {
        setCurrentStudentMajor(await getSubjects(event.target.value));
        console.log(event.target.value);
    };

    const handleFutureMajorSelect = async (event) => {
        setFutureStudentMajor(await getSubjects(event.target.value));
        console.log(event.target.value);
    };

    const handleFileUpload = (event) => {
        file = event.target.files[0];
        formData.append("file", file);
    };

    const handleFileUploadClick = () => {
        setIsLoading(true);
        if (!currentStudentMajor || !futureStudentMajor) {
            console.log(currentStudentMajor);
            console.log(futureStudentMajor);
            alert("Not enough data.");
            setIsLoading(false);
            return;
        }

        fetch("http://127.0.0.1:8000/api/extract", {
            // Your POST endpoint
            method: "POST",
            body: formData, // This is your file object
        })
            .then(
                (response) => response.json() // if the response is a JSON object
            )
            .then(
                (success) => {
                    success.student_current_major = currentStudentMajor;
                    success.student_future_major = futureStudentMajor;
                    setStudentData(success);
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
                    console.log(success);
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
                    <button onClick={handleFileUploadClick}>Confirm</button>
                </div>

                {isLoading && <p>Loading...</p>}
                {studentData && (
                    <div className="student-info">
                        <p>Student: {studentData.student_name}</p>
                        <h2>Trenutni smjer (prvi semestar):</h2>
                        {studentData.student_current_major[1].map((subject) => (
                            <div className="subject" key={subject.id}>
                                <p>{subject.name}</p>
                            </div>
                        ))}
                        <h2>
                            Smjer na koji se student prebacuje (prvi semestar):
                        </h2>
                        {studentData.student_future_major[1].map((subject) => (
                            <div className="subject" key={subject.id}>
                                <p>{subject.name}</p>
                            </div>
                        ))}
                        <h2>Ocjene:</h2>
                        <div className="student-grades">
                            {studentData.student_grades.map((grade) => (
                                <p key={grade}>{grade}</p>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default HomePage;
