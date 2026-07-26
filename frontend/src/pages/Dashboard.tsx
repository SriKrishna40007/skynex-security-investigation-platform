import Layout from "../components/layout/Layout";
import DashboardHeader from "../components/dashboard/DashboardHeader";
import StatsGrid from "../components/dashboard/StatsGrid";
import ExecutiveSummary from "../components/dashboard/ExecutiveSummary";

export default function Dashboard() {
  return (
    <Layout title="">
      <DashboardHeader />

      <StatsGrid />

      <ExecutiveSummary />
    </Layout>
  );
}
