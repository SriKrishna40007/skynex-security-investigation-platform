import type { ReactNode } from "react";

type LayoutProps = {
  title: string;
  children: ReactNode;
};

export default function Layout({
  title,
  children,
}: LayoutProps) {
  return (
    <section className="space-y-6">
      <header>
        <h2 className="text-2xl font-semibold tracking-tight text-white">
          {title}
        </h2>

        <p className="mt-1 text-sm text-slate-500">
          Security investigation workspace
        </p>
      </header>

      {children}
    </section>
  );
}
