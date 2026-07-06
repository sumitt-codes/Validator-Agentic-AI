import type { Metadata } from "next";
import "./globals.css";

// Fonts are declared in globals.css to match the generated standalone report.

export const metadata: Metadata = {
  title: "Startup Validator",
  description: "Autonomous market validation and investor report.",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
