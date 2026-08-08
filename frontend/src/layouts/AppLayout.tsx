import { Outlet } from "react-router-dom";

import Header from "@/components/layout/Header";
import Sidebar from "@/components/layout/Sidebar";

export default function AppLayout() {
  return (
    <div className="flex min-h-screen bg-[#050816] text-slate-100">
      <Sidebar />

      <div className="flex min-w-0 flex-1 flex-col">
        <Header />

        <main className="min-w-0 flex-1 overflow-auto">
          <div className="mx-auto w-full max-w-[1800px] p-6">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
}
