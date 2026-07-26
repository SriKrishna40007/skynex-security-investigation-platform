import SearchBar from "./SearchBar";
import NotificationButton from "./NotificationButton";
import UserMenu from "./UserMenu";

export default function DashboardHeader() {
  return (
    <header className="dashboard-header">
      <div>
        <h1>Dashboard</h1>

        <p className="dashboard-subtitle">
          Overview of your cloud security posture
        </p>
      </div>

      <div className="dashboard-actions">
        <SearchBar />

        <NotificationButton />

        <UserMenu />
      </div>
    </header>
  );
}
