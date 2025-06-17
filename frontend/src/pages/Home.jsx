import { useState } from "react";
import FileUploader from "../components/FileUploader";
import ReportViewer from "../components/ReportViewer";
import Loader from "../components/Loader";
import SearchReports from "../components/SearchReports";
import "../App.css";
const Home = () => {
  const [narrative, setNarrative] = useState("");
  const [loading, setLoading] = useState(false);

  const handleFileUpload = (narrative) => {
    setNarrative(narrative);
    setLoading(false);
  };

  const handleReportView = async (report) => {
    setLoading(true);
    try {
      ////const res = await fetch(`https://super-duper-winner-7vvjj4p6q756crqwr-8000.app.github.dev/reports/${id}`);
      //const data = await res.json();
      setNarrative(report.narrative || "[No narrative found]");
    } catch (err) {
      setNarrative(`[Error loading report: ${err.message}]`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div  className="container">
      <FileUploader onUpload={handleFileUpload} />
      <SearchReports onSelect={handleReportView} />
      {loading && <Loader />}
      <ReportViewer narrative={narrative} />
    </div>
  );
};

export default Home;
