import React from "react";
import {
    Document,
    Packer,
    Paragraph,
    TextRun,
    Table,
    TableCell,
    TableRow,
    WidthType,
} from "docx";
import FileSaver from "file-saver";

const Export = ({
    transferData,
    currentStudentMajorId,
    futureStudentMajorId,
    recognizedStudentSubjects,
    currentStudentMajor,
}) => {
    const findSubjectById = (id) => {
        if (!currentStudentMajor) return;
        let foundSubject;
        console.log("findSUbjectsbyID: ", id, currentStudentMajor);
        Object.keys(currentStudentMajor).forEach((semester) => {
            currentStudentMajor[semester].map((subject) => {
                if (subject.id == id) {
                    foundSubject = subject;
                }
            });
        });
        return foundSubject;
    };

    const calculateRequiredSubjects = (subject) => {
        let requiredSubjectsNames = "";
        console.log(transferData);

        if (!transferData) return;
        transferData
            .find((transfer) => transfer.recognizedSubject == subject.id)
            .requiredSubjects.forEach((sub) => {
                requiredSubjectsNames += `${findSubjectById(sub).name}, `;
            });
        return requiredSubjectsNames.slice(0, -2);
    };

    const calculateSubjectRow = (subject) => {
        let row = new TableRow({
            children: [
                new TableCell({
                    children: [
                        new Paragraph({
                            children: [
                                new TextRun({
                                    text: `${calculateRequiredSubjects(
                                        subject
                                    )}`,
                                    font: "Calibri",
                                }),
                            ],
                        }),
                    ],
                }),
                new TableCell({
                    children: [
                        new Paragraph({
                            children: [
                                new TextRun({
                                    text: `${subject.name}`,
                                    font: "Calibri",
                                }),
                            ],
                        }),
                    ],
                }),
                new TableCell({
                    children: [
                        new Paragraph({
                            children: [
                                new TextRun({
                                    text: `${subject.grade}`,
                                    font: "Calibri",
                                }),
                            ],
                            alignment: "center",
                        }),
                    ],
                }),
                new TableCell({
                    children: [
                        new Paragraph({
                            children: [
                                new TextRun({
                                    text: `${subject.ects}`,
                                    font: "Calibri",
                                }),
                            ],
                            alignment: "center",
                        }),
                    ],
                }),
            ],
        });
        return row;
    };

    const calculateSubjectRows = (semester) => {
        let rows = [];

        recognizedStudentSubjects[semester].forEach((subject) => {
            rows.push(calculateSubjectRow(subject));
        });
        return rows;
    };

    const calculateRows = () => {
        let rows = [];
        Object.keys(recognizedStudentSubjects).forEach((semester) => {
            rows.push(
                new TableRow({
                    children: [
                        new TableCell({
                            width: {
                                size: 14020,
                                type: WidthType.DXA,
                            },
                            columnSpan: [4],
                            children: [
                                new Paragraph({
                                    children: [
                                        new TextRun({
                                            text: `${semester}. Semestar`,
                                            bold: true,
                                            font: "Calibri",
                                        }),
                                    ],
                                    alignment: "center",
                                }),
                            ],
                        }),
                    ],
                })
            );
            rows.push(...calculateSubjectRows(semester));
        });
        return rows;
    };

    const calculateTable = () => {
        if (!recognizedStudentSubjects) return;

        let totalEcts = 0;
        Object.keys(recognizedStudentSubjects).forEach((semester) => {
            recognizedStudentSubjects[semester].forEach((subject) => {
                totalEcts += subject.ects;
            });
        });

        const table = new Table({
            columnWidths: [5505, 5505, 1505, 1505],
            rows: [
                new TableRow({
                    children: [
                        new TableCell({
                            width: {
                                size: 5505,
                                type: WidthType.DXA,
                            },
                            children: [
                                new Paragraph({
                                    children: [
                                        new TextRun({
                                            text: `Predmet na ${currentStudentMajorId}`,
                                            bold: true,
                                            font: "Calibri",
                                        }),
                                    ],
                                    alignment: "center",
                                }),
                            ],
                        }),
                        new TableCell({
                            width: {
                                size: 5505,
                                type: WidthType.DXA,
                            },
                            children: [
                                new Paragraph({
                                    children: [
                                        new TextRun({
                                            text: `Priznati predmet na ${futureStudentMajorId}`,
                                            bold: true,
                                            font: "Calibri",
                                        }),
                                    ],
                                    alignment: "center",
                                }),
                            ],
                        }),
                        new TableCell({
                            width: {
                                size: 1805,
                                type: WidthType.DXA,
                            },
                            children: [
                                new Paragraph({
                                    children: [
                                        new TextRun({
                                            text: "Ocjena",
                                            bold: true,
                                            font: "Calibri",
                                        }),
                                    ],
                                    alignment: "center",
                                }),
                            ],
                        }),
                        new TableCell({
                            width: {
                                size: 1505,
                                type: WidthType.DXA,
                            },
                            children: [
                                new Paragraph({
                                    children: [
                                        new TextRun({
                                            text: `ECTS`,
                                            bold: true,
                                            font: "Calibri",
                                        }),
                                    ],
                                    alignment: "center",
                                }),
                            ],
                        }),
                    ],
                }),
                ...calculateRows(),
                new TableRow({
                    children: [
                        new TableCell({
                            width: {
                                size: 14020,
                                type: WidthType.DXA,
                            },
                            columnSpan: [3],
                            children: [
                                new Paragraph({
                                    children: [
                                        new TextRun({
                                            text: `UKUPNO`,
                                            bold: true,
                                            font: "Calibri",
                                        }),
                                    ],
                                }),
                            ],
                        }),
                        new TableCell({
                            width: {
                                size: 1505,
                                type: WidthType.DXA,
                            },
                            children: [
                                new Paragraph({
                                    children: [
                                        new TextRun({
                                            text: `${totalEcts}`,
                                            font: "Calibri",
                                        }),
                                    ],
                                    alignment: "center",
                                }),
                            ],
                        }),
                    ],
                }),
            ],
        });
        return table;
    };

    const doc = new Document({
        paragraphStyles: [
            {
                id: "aside",
                name: "Aside",
                basedOn: "Normal",
                next: "Normal",
                run: {
                    backgroundColor: "58595a",
                    italics: true,
                },
            },
        ],
        sections: [
            {
                children: [calculateTable()],
            },
        ],
    });

    const handleExportClick = () => {
        Packer.toBlob(doc).then((buffer) => {
            FileSaver.saveAs(buffer, "Priznavanje.docx");
        });
    };

    return (
        <div className="Export">
            <div className="export-content">
                <button
                    className="export-button"
                    onClick={() => handleExportClick()}
                >
                    Preuzmi
                </button>
            </div>
        </div>
    );
};

export default Export;
