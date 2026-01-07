import React from 'react';
import { Github, Twitter, Linkedin, Heart } from 'lucide-react';

const Footer = () => {
    return (
        <footer className="bg-slate-50 border-t border-slate-200 pt-16 pb-8">
            <div className="max-w-7xl mx-auto px-6">
                <div className="grid grid-cols-1 md:grid-cols-4 gap-12 mb-16">
                    <div className="col-span-1 md:col-span-2 space-y-4">
                        <h3 className="text-xl font-bold text-slate-900">TUG<span className="text-purple-600">.</span></h3>
                        <p className="text-slate-500 max-w-sm leading-relaxed">
                            The Ultimate RAG Visualizer. A powerful educational platform to understand, visualize, and experiment with Retrieval Augmented Generation concepts in real-time.
                        </p>
                    </div>

                    <div className="space-y-4">
                        <h4 className="font-semibold text-slate-900">Platform</h4>
                        <ul className="space-y-2 text-sm text-slate-500">
                            <li><a href="/demo" className="hover:text-purple-600 transition-colors">Interactive Demo</a></li>
                            <li><a href="#" className="hover:text-purple-600 transition-colors">Vector Visualizer</a></li>
                            <li><a href="#" className="hover:text-purple-600 transition-colors">Chat Interface</a></li>
                            <li><a href="#" className="hover:text-purple-600 transition-colors">Analytics</a></li>
                        </ul>
                    </div>

                    <div className="space-y-4">
                        <h4 className="font-semibold text-slate-900">Connect</h4>
                        <div className="flex gap-4">
                            <a href="#" className="p-2 bg-white border border-slate-200 rounded-lg text-slate-500 hover:text-slate-900 hover:border-slate-300 transition-all shadow-sm">
                                <Github className="w-4 h-4" />
                            </a>
                            <a href="#" className="p-2 bg-white border border-slate-200 rounded-lg text-slate-500 hover:text-blue-400 hover:border-blue-200 transition-all shadow-sm">
                                <Twitter className="w-4 h-4" />
                            </a>
                            <a href="#" className="p-2 bg-white border border-slate-200 rounded-lg text-slate-500 hover:text-blue-700 hover:border-blue-200 transition-all shadow-sm">
                                <Linkedin className="w-4 h-4" />
                            </a>
                        </div>
                    </div>
                </div>

                <div className="border-t border-slate-200 pt-8 flex flex-col md:flex-row items-center justify-between gap-4 text-sm text-slate-400">
                    <p>&copy; 2025 The Ultimate RAG. Open Source.</p>
                </div>
            </div>
        </footer>
    );
};

export default Footer;
