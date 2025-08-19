import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { Providers } from './providers';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Intelligent Document Processing & Knowledge Base',
  description: 'AI-powered platform for document processing and knowledge management',
  keywords: 'document processing, AI, knowledge base, OCR, NLP',
  authors: [{ name: 'Document Processing Team' }],
  viewport: 'width=device-width, initial-scale=1',
  robots: 'index, follow',
  openGraph: {
    title: 'Intelligent Document Processing & Knowledge Base',
    description: 'AI-powered platform for document processing and knowledge management',
    type: 'website',
    locale: 'en_US',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Intelligent Document Processing & Knowledge Base',
    description: 'AI-powered platform for document processing and knowledge management',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
