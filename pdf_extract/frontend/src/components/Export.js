import React, { Component, useEffect, useRef } from "react";
import { useState } from "react";

const Export = ({
    student,
    transfer,
    requiredStudentSubjects,
    setRequiredStudentSubjects,
    recognizedStudentSubjects,
    setRecognizedStudentSubjects,
    currentStudentMajor,
    futureStudentMajor,
    setIsLoading,
}) => {
    const handleExportClick = () => {};

    return (
        <div className="Export">
            <div className="export-content">
                <button onClick={() => handleExportClick()}>Preuzmi</button>
            </div>
        </div>
    );
};

export default Export;
