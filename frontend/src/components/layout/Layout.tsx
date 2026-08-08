import type { ReactNode } from "react";
import Sidebar from "./Sidebar";

type LayoutProps = {
  title: string;
  children: ReactNode;
};

export default function Layout({
  title,
  children,
}: LayoutProps) {
  return (
    <div className="app">
      <Sidebar />

      <main className="content">
        <header className="page-header">
          <h2>{title}</h2>
        </header>

        {children}
      </main>
    </div>
  );
}
