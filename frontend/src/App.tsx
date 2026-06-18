import { useState } from "react";
import { api } from "./services/api";

function App() {
  const [fileInfo, setFileInfo] = useState<any>(null);
  const [validationResult, setValidationResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleFileUpload = async (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {

    const file = event.target.files?.[0];

    if (!file) return;

    setLoading(true);
    setValidationResult(null);
    setFileInfo(null);

    const formData = new FormData();
    formData.append("file", file);

    try {

      const uploadResponse = await api.post(
        "/upload",
        formData
      );

      setFileInfo(uploadResponse.data);

      const validationResponse =
        await api.post("/validate");

      setValidationResult(
        validationResponse.data
      );

      if (validationResponse.data.success) {

        

      }

    } catch (error) {

      console.error(error);
      alert("Processing failed");

    } finally {

      setLoading(false);

    }

  };


  return (
    <div className="min-h-screen bg-slate-100">
      <div className="max-w-7xl mx-auto p-8">

        <h1 className="text-5xl font-bold text-slate-800">
          Transaction Validation Platform
        </h1>

        <p className="mt-2 text-slate-600">
          Upload a transaction dataset and automatically validate, clean and process records.
        </p>

        <div className="grid grid-cols-4 gap-6 mt-10">

          <div className="bg-white rounded-xl shadow p-6">
            <h3 className="text-slate-500">
              Total Records
            </h3>

            <p className="text-3xl font-bold mt-2">
              {validationResult?.total_records || 0}
            </p>
          </div>

          <div className="bg-white rounded-xl shadow p-6">
            <h3 className="text-slate-500">
              Valid Records
            </h3>

            <p className="text-3xl font-bold mt-2 text-green-600">
              {validationResult?.valid_records || 0}
            </p>
          </div>

          <div className="bg-white rounded-xl shadow p-6">
            <h3 className="text-slate-500">
              Invalid Records
            </h3>

            <p className="text-3xl font-bold mt-2 text-red-600">
              {validationResult?.invalid_records || 0}
            </p>
          </div>

          <div className="bg-white rounded-xl shadow p-6">
            <h3 className="text-slate-500">
              Quality Score
            </h3>

            <p className="text-3xl font-bold mt-2">
              {validationResult?.quality_score || 0}%
            </p>

            {
              validationResult?.grade && (
                <p className="mt-2 font-semibold text-blue-600">
                  Grade: {validationResult.grade}
                </p>
              )
            }
          </div>

        </div>

        {
          validationResult && (

            <div className="bg-white rounded-xl shadow mt-8 p-6">

              {
                validationResult.success === false ? (

                  <>
                    <h2 className="text-2xl font-bold text-red-600">
                      ❌ Invalid Dataset Structure
                    </h2>

                    <p className="mt-4 font-semibold">
                      Missing Columns:
                    </p>

                    <ul className="list-disc ml-6 mt-2">

                      {
                        validationResult.missing_columns?.map(
                          (column: string) => (
                            <li key={column}>
                              {column}
                            </li>
                          )
                        )
                      }

                    </ul>
                  </>

                ) : (

                  <>
                    {
                      validationResult.invalid_records === 0 ? (

                        <>
                          <h2 className="text-2xl font-bold text-green-600">
                            ✅ Validation Successful
                          </h2>

                          <p className="mt-2">
                            Quality Score:
                            {" "}
                            {validationResult.quality_score}%
                          </p>
                        </>

                      ) : (

                        <>
                          <h2 className="text-2xl font-bold text-red-600">
                            ⚠ Validation Complete
                          </h2>

                          <p className="mt-2">
                            Found
                            {" "}
                            {validationResult.invalid_records}
                            {" "}
                            invalid records
                          </p>

                        </>

                      )
                    }

                    
                  </>

                )
              }

            </div>

          )
        }

        <div className="bg-white rounded-xl shadow mt-8 p-8">

          <h2 className="text-3xl font-bold mb-2">
            📄 Upload Transaction Dataset
          </h2>

          <p className="text-slate-500 mb-6">
            CSV and XLSX files supported
          </p>

          <input
            type="file"
            accept=".csv,.xlsx"
            onChange={handleFileUpload}
            className="mb-4"
          />
          {
            loading && (
              <div className="mt-4 text-blue-600 font-semibold">
                Processing dataset...
              </div>
            )
          }

          <br />

        
          {
            validationResult &&
            validationResult.success &&
            validationResult.cleaned_file && (

              <div className="mt-4">

                <div className="text-green-600 font-semibold mb-3">
                  ✓ Cleaned Dataset Generated
                </div>

                  <a
                    href="http://127.0.0.1:8000/api/download-latest-cleaned"
                    target="_blank"
                    rel="noreferrer"
                    className="bg-green-600 text-white px-6 py-2 rounded hover:bg-green-700"
                  >
                    ⬇ Download Cleaned Dataset
                  </a>

                  <a
                    href="http://127.0.0.1:8000/api/download-latest-report"
                    target="_blank"
                    rel="noreferrer"
                    className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700"
                  >
                    📊 Download Validation Report
                  </a>

              </div>

            )
          }

        </div>

        {fileInfo &&
         validationResult?.success !== false && (

          <div className="bg-white rounded-xl shadow mt-8 p-8">

            <h2 className="text-2xl font-semibold mb-4">
              Dataset Information
            </h2>

            <p>
              <strong>File:</strong> {fileInfo.file_name}
            </p>

            <p>
              <strong>Rows:</strong> {fileInfo.rows}
            </p>

            <p>
              <strong>Columns:</strong> {fileInfo.columns}
            </p>

            <div className="overflow-auto mt-6">

              <table className="min-w-full border">

                <thead>

                  <tr>

                    {fileInfo.column_names?.map(
                      (column: string) => (

                        <th
                          key={column}
                          className="border p-2 bg-slate-100"
                        >
                          {column}
                        </th>

                      )
                    )}

                  </tr>

                </thead>

                <tbody>

                  {fileInfo.preview?.map(
                    (row: any, index: number) => (

                      <tr key={index}>

                        {fileInfo.column_names?.map(
                          (column: string) => (

                            <td
                              key={column}
                              className="border p-2"
                            >
                              {String(row[column])}
                            </td>

                          )
                        )}

                      </tr>

                    )
                  )}

                </tbody>

              </table>

            </div>

          </div>

        )}

        {
          validationResult &&
          validationResult.errors &&
          validationResult.errors.length > 0 && (

            <div className="bg-white rounded-xl shadow mt-8 p-8">

              <h2 className="text-2xl font-semibold mb-4">
                Validation Summary
              </h2>

              <p>
                Processing Time:
                {" "}
                {validationResult.processing_time} sec
              </p>

              <p
                className={
                  validationResult.invalid_records > 0
                    ? "text-red-600 font-semibold mt-2"
                    : "text-green-600 font-semibold mt-2"
                }
              >
                Status:
                {" "}
                {
                  validationResult.invalid_records > 0
                    ? "Failed"
                    : "Passed"
                }
              </p>

            </div>

          )
        }

        {validationResult &&
          validationResult.errors &&
          validationResult.errors.length > 0 && (

            <div className="bg-white rounded-xl shadow mt-8 p-8">

              <h2 className="text-2xl font-semibold mb-4">
                Validation Errors
              </h2>

              <table className="min-w-full border">

                <thead>

                  <tr>

                    <th className="border p-2">
                      Row
                    </th>

                    <th className="border p-2">
                      Errors
                    </th>

                  </tr>

                </thead>

                <tbody>

                  {validationResult.errors.map(
                    (
                      error: any,
                      index: number
                    ) => (

                      <tr key={index}>

                        <td className="border p-2">
                          {error.row}
                        </td>

                        <td className="border p-2">
                          {error.errors.join(", ")}
                        </td>

                      </tr>

                    )
                  )}

                </tbody>

              </table>

            </div>

          )}

      
      <footer className="text-center py-10 text-slate-500">

        <p className="font-semibold">
          Transaction Validation Platform
        </p>

        <p className="text-sm mt-2">
          Automated data validation, quality assessment and processing.
        </p>

      </footer>
      </div>
    </div>
  );
}

export default App;