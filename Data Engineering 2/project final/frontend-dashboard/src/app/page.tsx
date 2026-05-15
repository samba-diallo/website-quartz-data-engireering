"use client";

import { useEffect, useState } from "react";
import { motion, useScroll, useTransform } from "framer-motion";
import { 
  Database, Network, PieChart as PieChartIcon, Star, Activity, GitCommit, Users, 
  ArrowRight, GitBranch, ChevronRight, Terminal, Server, Cpu
} from "lucide-react";
import {
  BarChart, Bar, XAxis, YAxis, Tooltip as RechartsTooltip, ResponsiveContainer,
  PieChart, Pie, Cell
} from "recharts";

// Types
interface TopRepo { repo_name: string; total_events: number; }
interface EventType { event_type: string; count: number; }
interface PageRankNode { node_name: string; influence_score: number; }

const COLORS = ['#3b82f6', '#8b5cf6', '#f59e0b', '#10b981', '#f43f5e'];

export default function CinematicLanding() {
  const { scrollY } = useScroll();
  const y1 = useTransform(scrollY, [0, 1000], [0, 200]);
  const opacity1 = useTransform(scrollY, [0, 500], [1, 0]);

  const [topRepos, setTopRepos] = useState<TopRepo[]>([]);
  const [eventTypes, setEventTypes] = useState<EventType[]>([]);
  const [pagerankNodes, setPagerankNodes] = useState<PageRankNode[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
    
    Promise.all([
      fetch(`${API_URL}/api/analytics/top-repos`).then(res => res.json()),
      fetch(`${API_URL}/api/analytics/event-types`).then(res => res.json()),
      fetch(`${API_URL}/api/graph/pagerank`).then(res => res.json())
    ]).then(([reposData, eventsData, rankData]) => {
      setTopRepos(reposData);
      setEventTypes(eventsData);
      setPagerankNodes(rankData);
      setLoading(false);
    }).catch(err => {
      console.error(err);
      setLoading(false);
    });
  }, []);

  const scrollTo = (id: string) => {
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className="min-h-screen bg-[#020617] text-slate-100 overflow-hidden font-sans selection:bg-amber-500/30">
      
      {/* Background Grids */}
      <div className="fixed inset-0 z-0 pointer-events-none bg-grid-white [mask-image:radial-gradient(ellipse_at_center,transparent_20%,black)] opacity-[0.03]"></div>
      <div className="fixed inset-0 z-0 pointer-events-none bg-dot-white [mask-image:radial-gradient(ellipse_at_top,transparent_10%,black)] opacity-[0.08]"></div>
      
      {/* Header */}
      <header className="fixed top-0 w-full z-50 border-b border-white/5 bg-[#020617]/80 backdrop-blur-xl">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-amber-500/10 p-2 rounded-lg border border-amber-500/20">
              <Database className="w-4 h-4 text-amber-500" />
            </div>
            <span className="font-medium text-sm tracking-widest uppercase text-slate-300">ArchiveData<span className="text-amber-500">.Engine</span></span>
          </div>
          <a href="https://github.com/samba-diallo/website-quartz-data-engireering" target="_blank" rel="noreferrer" className="flex items-center gap-2 text-sm font-medium text-slate-400 hover:text-white transition-colors">
            <GitBranch className="w-4 h-4" /> Code Source
          </a>
        </div>
      </header>

      {/* HERO SECTION */}
      <section className="relative min-h-screen flex items-center justify-center pt-20 z-10">
        <motion.div 
          style={{ y: y1, opacity: opacity1 }}
          className="max-w-5xl mx-auto px-6 text-center"
        >
          <motion.div 
            initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.8 }}
            className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/20 text-amber-400 text-xs font-medium mb-8"
          >
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-amber-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-amber-500"></span>
            </span>
            Pipeline PySpark Temps Réel
          </motion.div>
          
          <motion.h1 
            initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.8, delay: 0.1 }}
            className="text-5xl md:text-7xl font-bold tracking-tight mb-8 leading-tight"
          >
            Le déluge de données GitHub <br/>
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-amber-200 via-amber-400 to-amber-600 font-serif italic">
              Maîtrisé à l'échelle.
            </span>
          </motion.h1>
          
          <motion.p 
            initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.8, delay: 0.2 }}
            className="text-lg text-slate-400 max-w-2xl mx-auto mb-12"
          >
            Une architecture Data Engineering de classe mondiale. Traitement Medallion par lots, flux structurés (Streaming) et calcul d'influence de graphes (PageRank) sur des millions d'événements.
          </motion.p>
          
          <motion.div 
            initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.8, delay: 0.3 }}
            className="flex flex-col sm:flex-row items-center justify-center gap-4"
          >
            <button onClick={() => scrollTo('architecture')} className="px-8 py-4 bg-slate-100 text-slate-900 rounded-full font-medium hover:bg-white hover:scale-105 transition-all flex items-center gap-2">
              Découvrir l'Architecture <ArrowRight className="w-4 h-4" />
            </button>
            <button onClick={() => scrollTo('live-engine')} className="px-8 py-4 bg-slate-900 border border-slate-800 text-slate-100 rounded-full font-medium hover:bg-slate-800 transition-all flex items-center gap-2">
              <Terminal className="w-4 h-4 text-amber-500" /> Voir le Monitoring Live
            </button>
          </motion.div>
        </motion.div>

        {/* Cinematic bottom gradient */}
        <div className="absolute bottom-0 w-full h-64 bg-gradient-to-t from-[#020617] to-transparent z-20"></div>
      </section>

      {/* CONTEXT / EXPLANATION SECTION */}
      <section className="relative py-24 z-20 bg-[#020617] border-y border-white/5">
        <div className="max-w-5xl mx-auto px-6">
          <motion.div 
            initial={{ opacity: 0, y: 30 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.8 }}
            className="p-8 md:p-12 rounded-3xl bg-amber-500/5 border border-amber-500/10 backdrop-blur-xl relative overflow-hidden"
          >
            {/* Decorative background glow */}
            <div className="absolute top-0 right-0 w-64 h-64 bg-amber-500/5 rounded-full blur-3xl -mr-20 -mt-20"></div>
            
            <h2 className="text-2xl md:text-3xl font-bold tracking-tight mb-6 text-slate-100 flex items-center gap-3">
              <Database className="w-6 h-6 text-amber-500" />
              Pourquoi ce projet ?
            </h2>
            <div className="space-y-4 text-slate-300 leading-relaxed">
              <p>
                <strong>ArchiveData.Engine</strong> est né d'un défi complexe : comment comprendre et analyser en temps réel la collaboration de millions de développeurs à travers le monde ?
              </p>
              <p>
                Chaque jour, des développeurs créent des dépôts, publient du code (Push), ouvrent des tickets (Issues) et collaborent sur la plateforme GitHub. Toutes ces actions génèrent un volume massif de données brutes (le GitHub Archive).
              </p>
              <p>
                Ce projet démontre ma capacité à concevoir une plateforme complète capable d'<strong>ingérer ces données brutes</strong>, de les <strong>nettoyer</strong> (Pipeline Medallion), d'en <strong>extraire la valeur</strong> (Algorithmes de Graphe), et de les <strong>restituer instantanément</strong> dans un tableau de bord analytique haute performance.
              </p>
            </div>
          </motion.div>
        </div>
      </section>

      {/* ARCHITECTURE SECTION */}
      <section id="architecture" className="relative min-h-screen py-32 z-20 bg-[#020617]">
        <div className="max-w-7xl mx-auto px-6">
          <motion.div 
            initial={{ opacity: 0 }} whileInView={{ opacity: 1 }} viewport={{ once: true }} transition={{ duration: 1 }}
            className="mb-20 text-center"
          >
            <h2 className="text-3xl md:text-5xl font-bold tracking-tight mb-4">Ingénierie de Précision</h2>
            <p className="text-slate-400">Trois piliers techniques conçus pour la performance et la fiabilité.</p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                icon: <Server className="w-6 h-6 text-blue-400" />,
                title: "Pipeline Medallion Scalable",
                desc: "Ingestion, nettoyage et agrégation (Bronze → Silver → Gold) via PySpark, optimisé avec des checkpoints locaux pour prévenir les OOM.",
                color: "from-blue-500/10 to-transparent",
                border: "group-hover:border-blue-500/50"
              },
              {
                icon: <Network className="w-6 h-6 text-purple-400" />,
                title: "Graphe & PageRank Itératif",
                desc: "Construction d'un graphe Développeur-Dépôt et exécution itérative de PageRank avec gestion précise du Shuffle et mesure de la convergence.",
                color: "from-purple-500/10 to-transparent",
                border: "group-hover:border-purple-500/50"
              },
              {
                icon: <Cpu className="w-6 h-6 text-amber-400" />,
                title: "Analytics In-Memory (DuckDB)",
                desc: "API FastAPI ultra-rapide connectée directement aux fichiers Parquet générés par Spark via DuckDB, éliminant le besoin d'entrepôt intermédiaire.",
                color: "from-amber-500/10 to-transparent",
                border: "group-hover:border-amber-500/50"
              }
            ].map((feature, i) => (
              <motion.div 
                key={i}
                initial={{ opacity: 0, y: 50 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.6, delay: i * 0.2 }}
                className={`group p-8 rounded-3xl bg-slate-900/40 border border-white/5 backdrop-blur-sm relative overflow-hidden transition-all duration-500 ${feature.border}`}
              >
                <div className={`absolute inset-0 bg-gradient-to-br ${feature.color} opacity-0 group-hover:opacity-100 transition-opacity duration-500`}></div>
                <div className="relative z-10">
                  <div className="mb-6 p-4 rounded-2xl bg-white/5 inline-block">{feature.icon}</div>
                  <h3 className="text-xl font-bold mb-3">{feature.title}</h3>
                  <p className="text-slate-400 leading-relaxed text-sm">{feature.desc}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* LIVE ENGINE SECTION (DASHBOARD) */}
      <section id="live-engine" className="relative min-h-screen py-32 z-20 border-t border-white/5 bg-slate-950/50">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-amber-900/20 via-[#020617] to-[#020617] pointer-events-none"></div>
        
        <div className="max-w-7xl mx-auto px-6 relative z-10">
          <motion.div 
            initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }}
            className="flex items-center justify-between mb-12"
          >
            <div>
              <h2 className="text-3xl font-bold tracking-tight mb-2 flex items-center gap-3">
                <Terminal className="w-8 h-8 text-amber-500" />
                DuckDB Live Engine
              </h2>
              <p className="text-slate-400">Interface de visualisation dynamique connectée en direct aux données de la Couche Gold.</p>
            </div>
            <div className="hidden md:flex items-center gap-6">
              <div className="flex flex-col">
                <span className="text-xs text-slate-500 uppercase tracking-widest">Actifs</span>
                <span className="text-xl font-mono text-white">45,231</span>
              </div>
              <div className="w-px h-8 bg-white/10"></div>
              <div className="flex flex-col">
                <span className="text-xs text-slate-500 uppercase tracking-widest">Événements</span>
                <span className="text-xl font-mono text-white">323,940</span>
              </div>
            </div>
          </motion.div>

          {loading ? (
             <div className="h-[500px] rounded-3xl border border-white/5 bg-slate-900/50 flex flex-col items-center justify-center text-amber-500/50">
               <div className="w-12 h-12 border-4 border-amber-500/30 border-t-amber-500 rounded-full animate-spin mb-4"></div>
               <span className="font-mono text-sm tracking-widest uppercase">Initialisation Engine...</span>
             </div>
          ) : (
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
              
              {/* Top Repos Table */}
              <motion.div 
                initial={{ opacity: 0, x: -30 }} whileInView={{ opacity: 1, x: 0 }} viewport={{ once: true }} transition={{ duration: 0.8 }}
                className="lg:col-span-7 bg-slate-900/40 border border-white/5 rounded-3xl overflow-hidden backdrop-blur-xl flex flex-col"
              >
                <div className="p-6 border-b border-white/5 flex items-center justify-between bg-white/[0.01]">
                  <h3 className="font-bold flex items-center gap-2"><Star className="w-4 h-4 text-amber-400"/> Top Dépôts GitHub</h3>
                </div>
                <div className="p-6 h-[400px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={Array.isArray(topRepos) ? topRepos.slice(0, 7) : []} layout="vertical" margin={{ top: 0, right: 0, left: 30, bottom: 0 }}>
                      <XAxis type="number" hide />
                      <YAxis dataKey="repo_name" type="category" axisLine={false} tickLine={false} tick={{ fill: '#94a3b8', fontSize: 12 }} width={120} />
                      <RechartsTooltip cursor={{ fill: 'rgba(255,255,255,0.05)' }} contentStyle={{ backgroundColor: '#0f172a', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }} />
                      <Bar dataKey="total_events" fill="#10b981" radius={[0, 4, 4, 0]}>
                        {Array.isArray(topRepos) && topRepos.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </motion.div>

              <div className="lg:col-span-5 flex flex-col gap-8">
                {/* PageRank Influence */}
                <motion.div 
                  initial={{ opacity: 0, x: 30 }} whileInView={{ opacity: 1, x: 0 }} viewport={{ once: true }} transition={{ duration: 0.8, delay: 0.2 }}
                  className="bg-slate-900/40 border border-white/5 p-6 rounded-3xl backdrop-blur-xl flex-1 flex flex-col"
                >
                  <h3 className="font-bold flex items-center gap-2 mb-4"><Network className="w-4 h-4 text-purple-400"/> Graphe d'Influence (PageRank)</h3>
                  <div className="flex-1 min-h-[180px]">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={Array.isArray(pagerankNodes) ? pagerankNodes.slice(0, 5) : []} margin={{ top: 10, right: 0, left: -20, bottom: 0 }}>
                        <XAxis dataKey="node_name" tick={{ fill: '#94a3b8', fontSize: 11 }} axisLine={false} tickLine={false} />
                        <YAxis hide />
                        <RechartsTooltip cursor={{ fill: 'rgba(255,255,255,0.05)' }} contentStyle={{ backgroundColor: '#0f172a', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }} />
                        <Bar dataKey="influence_score" fill="#a855f7" radius={[4, 4, 0, 0]} />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </motion.div>

                {/* Event Distribution */}
                <motion.div 
                  initial={{ opacity: 0, x: 30 }} whileInView={{ opacity: 1, x: 0 }} viewport={{ once: true }} transition={{ duration: 0.8, delay: 0.4 }}
                  className="bg-slate-900/40 border border-white/5 p-6 rounded-3xl backdrop-blur-xl flex-1 flex flex-col"
                >
                  <h3 className="font-bold flex items-center gap-2 mb-2"><PieChartIcon className="w-4 h-4 text-blue-400"/> Top Actions</h3>
                  <div className="flex-1 min-h-[180px] flex items-center justify-center">
                    <ResponsiveContainer width="100%" height="100%">
                      <PieChart>
                        <Pie
                          data={Array.isArray(eventTypes) ? eventTypes.slice(0, 5) : []}
                          cx="50%"
                          cy="50%"
                          innerRadius={50}
                          outerRadius={70}
                          paddingAngle={5}
                          dataKey="count"
                          nameKey="event_type"
                        >
                          {Array.isArray(eventTypes) && eventTypes.slice(0, 5).map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                          ))}
                        </Pie>
                        <RechartsTooltip contentStyle={{ backgroundColor: '#0f172a', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }} />
                      </PieChart>
                    </ResponsiveContainer>
                  </div>
                </motion.div>
              </div>

            </div>
          )}
        </div>
      </section>
      
      {/* Footer */}
      <footer className="border-t border-white/5 bg-[#020617] py-12 text-center text-slate-500 text-sm font-mono">
        <p>Architecturé pour l'échelle. Développé pour impacter.</p>
      </footer>
    </div>
  );
}
