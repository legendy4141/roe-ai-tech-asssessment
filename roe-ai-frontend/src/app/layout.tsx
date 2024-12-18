import "./styles/globals.css";

export const metadata = {
  title: "Roe AI Video App",
  description: "A video analysis platform with search and upload features",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <header className="bg-gradient-to-r from-blue-600 to-purple-500 shadow-md">
          <h1 className="text-4xl font-extrabold tracking-tight text-center py-4">Roe AI Video Platform</h1>
        </header>
        <main className="container mx-auto px-6 py-8">{children}</main>
      </body>
    </html>
  );
}
