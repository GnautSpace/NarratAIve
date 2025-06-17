import ReactMarkdown from 'react-markdown';
import "../App.css";
const ReportViewer=({narrative})=>{
    if(!narrative) return null;
    return(
        <div className="card" style={{ whiteSpace: "pre-wrap", fontSize: "14px", lineHeight: "1.6" }}>
            <h2>AI-Generated Report</h2>
            <ReactMarkdown>{narrative}</ReactMarkdown>
        </div>
    )

}
export default ReportViewer;