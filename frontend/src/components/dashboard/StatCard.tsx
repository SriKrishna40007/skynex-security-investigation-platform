type StatCardProps = {
  title: string;
  value: string | number;
};

export default function StatCard({
  title,
  value,
}: StatCardProps) {
  return (
    <article className="rounded-2xl border border-white/[0.07] bg-[#0b1222] p-5 transition hover:border-white/[0.12]">
      <p className="text-sm text-slate-500">
        {title}
      </p>

      <p className="mt-4 text-3xl font-semibold tracking-tight text-white">
        {value}
      </p>
    </article>
  );
}
