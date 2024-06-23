import React, { Component, useEffect, useRef } from "react";
import { useState } from "react";
import HomePage from "./HomePage";

const RecognizedSubjects = ({
    student,
    transfer,
    requiredStudentSubjects,
    setRequiredStudentSubjects,
    recognizedStudentSubjects,
    setRecognizedStudentSubjects,
    currentStudentMajor,
    futureStudentMajor,
    isLoading,
    setIsLoading,
}) => {
    useEffect(() => {
        getRecognizedSubjects(student, transfer);
    }, [student]);

    const getRecognizedSubjects = async (student, transfer) => {
        let requiredSubjects = [];
        let temp;
        let tempGrades = [];
        let matches;
        let recognizedSubjects = [];
        let transferData = [];

        await fetch("http://127.0.0.1:8000/api/get-transfer-data", {
            method: "POST",
            body: transfer,
        })
            .then(
                (response) => response.json() // if the response is a JSON object
            )
            .then(
                (success) => {
                    transferData = success;
                    setIsLoading(false);
                } // Handle the success response object
            )
            .catch(
                (error) => console.log(error) // Handle the error response object
            );

        for (const x in currentStudentMajor) {
            for (const y in currentStudentMajor[x]) {
                for (const z in student.student_grades) {
                    if (
                        currentStudentMajor[x][y].name ==
                        student.student_grades[z].name
                    ) {
                        console.log("Match: ", currentStudentMajor[x][y].name);
                        temp = currentStudentMajor[x][y];
                        temp.grade = student.student_grades[z].grade;
                        requiredSubjects.push(temp);
                    }
                }
            }
        }

        console.log(
            "Subjects that match the current major: ",
            requiredSubjects
        );

        for (const i in transferData) {
            matches = 0;
            for (const j in transferData[i].requiredSubjects) {
                for (const k in requiredSubjects) {
                    if (
                        transferData[i].requiredSubjects[j] ==
                        requiredSubjects[k].id
                    ) {
                        matches++;
                        tempGrades.push(requiredSubjects[k].grade);

                        if (
                            matches == transferData[i].requiredSubjects.length
                        ) {
                            console.log(
                                "Recognized subject: ",
                                transferData[i].recognizedSubject
                            );

                            for (const l in futureStudentMajor) {
                                for (const m in futureStudentMajor[l]) {
                                    if (
                                        transferData[i].recognizedSubject ==
                                        futureStudentMajor[l][m].id
                                    ) {
                                        temp = futureStudentMajor[l][m];
                                        temp.grade = 0;
                                        for (const ind in tempGrades) {
                                            temp.grade =
                                                Number(temp.grade) +
                                                Number(tempGrades[ind]);
                                        }
                                        temp.grade = Math.round(
                                            temp.grade / tempGrades.length
                                        );
                                        recognizedSubjects.push(temp);
                                        tempGrades = [];
                                        break;
                                    }
                                }
                            }
                        }

                        break;
                    }
                }
            }
        }

        console.log(
            "Required: ",
            requiredSubjects,
            "Recognized",
            recognizedSubjects
        );

        setRequiredStudentSubjects(requiredSubjects);
        setRecognizedStudentSubjects(recognizedSubjects);
    };

    return (
        <div className="RecognizedSubjects">
            <div className="recognized-subjects-content">
                <div className="transfer-block">
                    <div className="current-student-major">
                        <h2>Smjer sa kojeg se student prebacuje: </h2>
                        {requiredStudentSubjects &&
                            Object.keys(currentStudentMajor).map(
                                (keyName, i) => (
                                    <React.Fragment key={i}>
                                        <div className="current-student-major-semester">
                                            <h3>{keyName}. semestar</h3>
                                            {currentStudentMajor[keyName].map(
                                                (subject, index) => (
                                                    <div
                                                        className="passed-subject"
                                                        key={index}
                                                    >
                                                        <p>{subject.name}</p>
                                                        <input
                                                            type="text"
                                                            defaultValue={
                                                                requiredStudentSubjects[
                                                                    requiredStudentSubjects.findIndex(
                                                                        (x) =>
                                                                            x.id ==
                                                                            subject.id
                                                                    )
                                                                ] &&
                                                                requiredStudentSubjects[
                                                                    requiredStudentSubjects.findIndex(
                                                                        (x) =>
                                                                            x.id ==
                                                                            subject.id
                                                                    )
                                                                ].grade
                                                            }
                                                        ></input>
                                                    </div>
                                                )
                                            )}
                                        </div>
                                    </React.Fragment>
                                )
                            )}
                    </div>

                    <div className="recognized-student-grades">
                        <h2>Priznate ocjene:</h2>
                        {recognizedStudentSubjects &&
                            recognizedStudentSubjects.map((subject) => (
                                <p key={subject.name}>
                                    {subject.name} | Ocjena: {subject.grade}
                                </p>
                            ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default RecognizedSubjects;
