import { useParams } from "react-router-dom";
import ExperimentDetailView from "../components/Experiments/ExperimentDetailView";

export default function ExperimentDetail() {
  const { id } = useParams();
  return <ExperimentDetailView experimentId={id} />;
}