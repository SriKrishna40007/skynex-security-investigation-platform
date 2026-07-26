type HeaderProps = {
  title: string;
};

export default function Header({ title }: HeaderProps) {
  return (
    <header className="page-header">
      <h2>{title}</h2>
    </header>
  );
}
