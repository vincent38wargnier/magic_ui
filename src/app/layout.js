import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

export const metadata = {
  title: "mcpmyapi.com - Transform Your APIs into MCP Servers",
  description: "Seamlessly convert your APIs into MCP servers. Run directly on your servers or use our SaaS platform. FastAPI package available.",
  keywords: "API, MCP server, FastAPI, API transformation, SaaS, developer tools",
  authors: [{ name: "mcpmyapi.com" }],
  viewport: "width=device-width, initial-scale=1",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" className="scroll-smooth">
      <body className={`${inter.variable} font-sans antialiased`}>
        {children}
      </body>
    </html>
  );
}
