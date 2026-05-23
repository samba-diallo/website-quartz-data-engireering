"use client";

import React, { useState, useEffect } from 'react';
import {
  TrendingUp, Users, Activity, Package, Terminal, Search,
  Bell, ChevronRight, LayoutDashboard, Database, Zap, Settings,
  Sun, Moon, HelpCircle, BookOpen, AlertCircle, Workflow
} from 'lucide-react';
import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, PieChart, Pie, Cell
} from 'recharts';
import { motion } from 'framer-motion';

// --- Types ---
interface TopRepo {
  name: string;
  activity: number;
  color?: string;
}

interface ActivityPoint {
  time: string;
  commits: number;
  prs: number;
}

interface InfluenceScore {
  name: string;
  value: number;
}

interface AnalyticsData {
  total_events: number;
  active_users: number;
  top_repos: TopRepo[];
  activity_over_time: ActivityPoint[];
  influence_scores: InfluenceScore[];
  data_coverage?: string;
}

interface StatCardProps {
  title: string;
  value: string | undefined;
  change: string;
  icon: React.ComponentType<{ size?: number; className?: string }>;
  delay: number;
}

const StatCard = ({ title, value, change, icon: Icon, delay }: StatCardProps) => (
  <motion.div 
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ delay, duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
    className="glass p-6 relative overflow-hidden group cursor-default"
  >
    <div className="flex justify-between items-start">
      <div>
        <p className="text-text-dim text-xs font-semibold uppercase tracking-wider mb-2 font-heading">{title}</p>
        <h3 className="text-3xl font-bold font-heading text-text-main group-hover:text-primary-gold transition-colors duration-500">{value}</h3>
        <div className="flex items-center mt-2 space-x-1">
          <span className={`text-xs font-medium ${change.startsWith('+') ? 'text-accent-emerald-bright' : 'text-red-400'}`}>
            {change}
          </span>
          <span className="text-text-dim text-[10px] uppercase">vs last hour</span>
        </div>
      </div>
      <div className="p-3 rounded-xl bg-bg-deep border border-border-subtle group-hover:border-primary-gold transition-colors duration-500">
        <Icon size={20} className="text-primary-gold" />
      </div>
    </div>
    {/* Animated background glow */}
    <div className="absolute -bottom-8 -right-8 w-24 h-24 bg-primary-gold opacity-0 group-hover:opacity-10 blur-3xl transition-opacity duration-700 rounded-full" />
  </motion.div>
);

type LucideIcon = React.ComponentType<{ size?: number; className?: string }>;

interface SidebarItemProps {
  icon: LucideIcon;
  label: string;
  active?: boolean;
  onClick?: () => void;
}

const SidebarItem = ({ icon: Icon, label, active = false, onClick }: SidebarItemProps) => (
  <div
    onClick={onClick}
    className={`flex items-center space-x-3 p-3 rounded-xl cursor-pointer transition-all duration-300 group ${active ? 'bg-primary-gold-muted text-primary-gold' : 'text-text-dim hover:text-text-main hover:bg-white/5'}`}
  >
    <Icon size={18} className={active ? 'text-primary-gold' : 'group-hover:scale-110 transition-transform'} />
    <span className="text-sm font-medium">{label}</span>
  </div>
);

type ViewKey = 'global-pulse' | 'data-sources' | 'kafka-streams' | 'spark-jobs' | 'help';

interface PlaceholderItem {
  name: string;
  status: string;
  detail: string;
}

interface PlaceholderViewProps {
  title: string;
  subtitle: string;
  icon: LucideIcon;
  items: PlaceholderItem[];
}

const PlaceholderView = ({ title, subtitle, icon: Icon, items }: PlaceholderViewProps) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
    className="glass p-8"
  >
    <div className="flex items-center space-x-4 mb-8">
      <div className="p-4 rounded-2xl bg-bg-deep border border-border-subtle">
        <Icon size={28} className="text-primary-gold" />
      </div>
      <div>
        <h3 className="text-2xl font-bold font-heading">{title}</h3>
        <p className="text-text-dim text-sm">{subtitle}</p>
      </div>
    </div>

    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {items.map((item, idx) => (
        <div key={idx} className="p-5 rounded-2xl border border-border-subtle bg-bg-surface/40 hover:border-primary-gold/40 transition-colors">
          <div className="flex justify-between items-start mb-2">
            <p className="text-sm font-bold text-text-main">{item.name}</p>
            <span className={`text-[10px] font-bold uppercase tracking-tighter px-2 py-1 rounded-full ${item.status === 'active' ? 'text-accent-emerald-bright bg-accent-emerald/30' : 'text-text-dim bg-bg-deep'}`}>
              {item.status}
            </span>
          </div>
          <p className="text-xs text-text-dim leading-relaxed">{item.detail}</p>
        </div>
      ))}
    </div>
  </motion.div>
);

interface LayerStatus {
  active: boolean;
  files: number;
  last_update: string | null;
}

interface PipelineStatus {
  bronze: LayerStatus;
  silver: LayerStatus;
  gold: LayerStatus;
}

const formatRelative = (iso: string | null): string => {
  if (!iso) return '—';
  const diff = Date.now() - new Date(iso).getTime();
  if (diff < 0) return 'just now';
  const minutes = Math.floor(diff / 60000);
  if (minutes < 1) return 'just now';
  if (minutes < 60) return `${minutes}m ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}h ago`;
  return `${Math.floor(hours / 24)}d ago`;
};

const PipelineStatusPanel = () => {
  const [status, setStatus] = useState<PipelineStatus | null>(null);

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
        const response = await fetch(`${apiUrl}/api/analytics/pipeline-status`);
        if (response.ok) setStatus(await response.json());
      } catch {
        // silent — UI shows '—' on missing data
      }
    };
    fetchStatus();
    const interval = setInterval(fetchStatus, 30000);
    return () => clearInterval(interval);
  }, []);

  const layers: { key: keyof PipelineStatus; label: string }[] = [
    { key: 'bronze', label: 'Bronze' },
    { key: 'silver', label: 'Silver' },
    { key: 'gold', label: 'Gold' },
  ];

  const latest = status
    ? [status.bronze.last_update, status.silver.last_update, status.gold.last_update]
        .filter((t): t is string => !!t)
        .sort()
        .pop() ?? null
    : null;

  return (
    <div className="glass p-4 rounded-2xl">
      <div className="flex justify-between items-center mb-3">
        <p className="text-xs text-primary-gold font-bold uppercase tracking-wider">Pipeline Status</p>
        <span className="relative flex h-2 w-2">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-accent-emerald-bright opacity-60" />
          <span className="relative inline-flex rounded-full h-2 w-2 bg-accent-emerald-bright" />
        </span>
      </div>

      <div className="space-y-2 mb-3">
        {layers.map(({ key, label }) => {
          const layer = status?.[key];
          const active = layer?.active ?? false;
          return (
            <div key={key} className="flex justify-between items-center text-[11px]">
              <span className="text-text-muted">{label}</span>
              <div className="flex items-center space-x-2">
                <span className="font-mono text-text-dim">{layer ? `${layer.files} files` : '…'}</span>
                <span className={`w-1.5 h-1.5 rounded-full ${active ? 'bg-accent-emerald-bright' : 'bg-text-dim'}`} />
              </div>
            </div>
          );
        })}
      </div>

      <div className="pt-3 border-t border-border-subtle">
        <p className="text-[10px] text-text-dim">
          Last sync <span className="font-mono text-text-muted">{formatRelative(latest)}</span>
        </p>
      </div>
    </div>
  );
};

const HelpView = () => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
    className="space-y-6"
  >
    {/* Intro */}
    <div className="glass p-8">
      <div className="flex items-center space-x-4 mb-6">
        <div className="p-4 rounded-2xl bg-bg-deep border border-border-subtle">
          <BookOpen size={28} className="text-primary-gold" />
        </div>
        <div>
          <h3 className="text-2xl font-bold font-heading">C&apos;est quoi ce dashboard ?</h3>
          <p className="text-text-dim text-sm">En quelques phrases simples</p>
        </div>
      </div>
      <p className="text-text-muted leading-relaxed">
        Ce dashboard affiche en temps réel <span className="text-primary-gold font-bold">ce qui se passe sur GitHub</span>,
        la plus grande plateforme de code au monde. Toutes les heures, des millions de développeurs créent, modifient
        et partagent du code. Notre pipeline collecte ces événements, les nettoie, les agrège, puis te montre les
        résultats sous forme de chiffres et de graphiques.
      </p>
    </div>

    {/* Les KPI */}
    <div className="glass p-8">
      <div className="flex items-center space-x-3 mb-6">
        <TrendingUp size={20} className="text-primary-gold" />
        <h3 className="text-lg font-bold font-heading">Les 4 chiffres en haut (les KPI)</h3>
      </div>
      <div className="space-y-4">
        <div className="p-4 rounded-xl bg-bg-surface/40 border border-border-subtle">
          <div className="flex items-center space-x-2 mb-1">
            <Users size={14} className="text-primary-gold" />
            <p className="text-sm font-bold text-text-main">Active Developers</p>
          </div>
          <p className="text-xs text-text-muted leading-relaxed">
            Combien de personnes uniques (comptes GitHub distincts) ont fait quelque chose dans
            les données traitées. Calculé en temps réel depuis la couche Bronze de notre pipeline.
          </p>
        </div>
        <div className="p-4 rounded-xl bg-bg-surface/40 border border-border-subtle">
          <div className="flex items-center space-x-2 mb-1">
            <TrendingUp size={14} className="text-primary-gold" />
            <p className="text-sm font-bold text-text-main">Signal Volume</p>
          </div>
          <p className="text-xs text-text-muted leading-relaxed">
            Nombre total d&apos;événements traités depuis le démarrage du pipeline.
            Un &laquo; événement &raquo; = une action (commit, ouverture d&apos;une pull request, commentaire, etc.).
          </p>
        </div>
        <div className="p-4 rounded-xl bg-bg-surface/40 border border-border-subtle">
          <div className="flex items-center space-x-2 mb-1">
            <Zap size={14} className="text-primary-gold" />
            <p className="text-sm font-bold text-text-main">Throughput</p>
          </div>
          <p className="text-xs text-text-muted leading-relaxed">
            Vitesse de traitement : combien d&apos;événements par seconde le système avale.
            Plus c&apos;est haut, plus le pipeline est performant.
          </p>
        </div>
        <div className="p-4 rounded-xl bg-bg-surface/40 border border-border-subtle">
          <div className="flex items-center space-x-2 mb-1">
            <Package size={14} className="text-primary-gold" />
            <p className="text-sm font-bold text-text-main">Data Layers</p>
          </div>
          <p className="text-xs text-text-muted leading-relaxed">
            Où on en est dans le traitement. <span className="text-primary-gold">Bronze</span> = brut,
            tel qu&apos;il arrive. <span className="text-primary-gold">Silver</span> = nettoyé.
            <span className="text-primary-gold"> Gold</span> = prêt à être affiché.
          </p>
        </div>
      </div>
    </div>

    {/* Les graphiques */}
    <div className="glass p-8">
      <div className="flex items-center space-x-3 mb-6">
        <Activity size={20} className="text-primary-gold" />
        <h3 className="text-lg font-bold font-heading">Les graphiques au milieu</h3>
      </div>
      <div className="space-y-5">
        <div>
          <p className="text-sm font-bold text-text-main mb-2">Global Activity Trends (la grande courbe)</p>
          <p className="text-xs text-text-muted leading-relaxed">
            Montre l&apos;activité au fil des heures.
            La courbe <span className="text-primary-gold font-bold">or</span> = les <em>commits</em> (sauvegardes de code).
            La courbe <span className="text-accent-emerald-bright font-bold">verte pointillée</span> = les <em>pull requests</em>
            (propositions de modifications soumises par les développeurs).
          </p>
        </div>
        <div className="border-t border-border-subtle pt-5">
          <p className="text-sm font-bold text-text-main mb-2">Ecosystem Influence (le donut à droite)</p>
          <p className="text-xs text-text-muted leading-relaxed">
            Camembert qui montre quels types d&apos;actions sont les plus courants.
            En général <em>Push</em> (sauvegarde de code) domine largement, suivi de <em>Create</em> (création de branche/repo),
            <em> PullRequest</em> (proposition de modif) et <em>IssueComment</em> (commentaire sur un problème).
          </p>
        </div>
        <div className="border-t border-border-subtle pt-5">
          <p className="text-sm font-bold text-text-main mb-2">Trending Architectural Units (le tableau en bas)</p>
          <p className="text-xs text-text-muted leading-relaxed">
            Les dépôts de code les plus actifs sur la période, classés du plus à intense au moins intense.
            Le chiffre à droite = nombre d&apos;événements observés pour ce dépôt.
          </p>
        </div>
      </div>
    </div>

    {/* Pipeline Status */}
    <div className="glass p-8">
      <div className="flex items-center space-x-3 mb-6">
        <Workflow size={20} className="text-primary-gold" />
        <h3 className="text-lg font-bold font-heading">Le petit panneau &laquo; Pipeline Status &raquo; en bas à gauche</h3>
      </div>
      <p className="text-text-muted text-sm leading-relaxed mb-4">
        Ce panneau montre l&apos;état des 3 couches de stockage de données.
        Le point <span className="text-accent-emerald-bright">vert qui clignote</span> indique que le pipeline est actif.
      </p>
      <div className="space-y-3 text-xs text-text-muted">
        <div className="flex items-start space-x-3">
          <span className="text-primary-gold font-bold w-16 shrink-0">Bronze</span>
          <span>Les données brutes, telles qu&apos;elles sortent de GitHub. Aucun traitement, juste un dépôt.</span>
        </div>
        <div className="flex items-start space-x-3">
          <span className="text-primary-gold font-bold w-16 shrink-0">Silver</span>
          <span>Les données nettoyées : on a enlevé les doublons, formaté les dates, retiré les champs inutiles.</span>
        </div>
        <div className="flex items-start space-x-3">
          <span className="text-primary-gold font-bold w-16 shrink-0">Gold</span>
          <span>Les données agrégées et prêtes à être affichées (top repos, distribution des événements, etc.).</span>
        </div>
      </div>
      <p className="text-[11px] text-text-dim mt-4">
        &laquo; Last sync &raquo; indique quand le pipeline a été mis à jour pour la dernière fois.
      </p>
    </div>

    {/* Comment on calcule Active Developers */}
    <div className="glass p-8 border border-accent-emerald-bright/20">
      <div className="flex items-center space-x-3 mb-4">
        <AlertCircle size={20} className="text-accent-emerald-bright" />
        <h3 className="text-lg font-bold font-heading">D&apos;où vient le chiffre &laquo; Active Developers &raquo; ?</h3>
      </div>
      <p className="text-text-muted text-sm leading-relaxed mb-3">
        Pour compter les développeurs uniques, le backend fait une requête SQL en direct
        sur la couche <span className="text-primary-gold">Bronze</span> du data lake :
      </p>
      <pre className="text-[11px] font-mono text-text-muted bg-bg-deep p-3 rounded-lg overflow-x-auto border border-border-subtle">
{`SELECT COUNT(DISTINCT actor_login)
FROM bronze_v2/**/*.parquet
WHERE actor_login IS NOT NULL`}
      </pre>
      <p className="text-xs text-text-muted leading-relaxed mt-3">
        Chaque événement GitHub (commit, PR, comment...) contient le pseudo de la personne
        qui l&apos;a déclenché. On compte les pseudos uniques, et voilà.
        Pas de calcul Gold pré-agrégé : c&apos;est lu en temps réel depuis le streaming Bronze
        (1.5M+ events ingérés).
      </p>
    </div>

    {/* Coulisses */}
    <div className="glass p-8">
      <div className="flex items-center space-x-3 mb-6">
        <Terminal size={20} className="text-primary-gold" />
        <h3 className="text-lg font-bold font-heading">Comment ça marche en coulisses ?</h3>
      </div>
      <p className="text-text-muted text-sm leading-relaxed mb-4">
        Imagine une usine de recyclage d&apos;eau, mais pour les données :
      </p>
      <ol className="space-y-3 text-xs text-text-muted leading-relaxed list-decimal list-inside">
        <li><span className="text-text-main font-bold">GitHub Archive</span> publie un fichier toutes les heures avec tous les événements publics.</li>
        <li>Notre <span className="text-text-main font-bold">producer</span> télécharge ce fichier et le verse dans <span className="text-text-main font-bold">Kafka</span> (une file d&apos;attente géante).</li>
        <li><span className="text-text-main font-bold">Spark Streaming</span> lit Kafka 24h/24 et écrit chaque événement dans la couche <em>Bronze</em>.</li>
        <li><span className="text-text-main font-bold">Airflow</span> déclenche le nettoyage (Silver) puis les agrégations (Gold) à intervalles réguliers.</li>
        <li>Le <span className="text-text-main font-bold">backend FastAPI</span> lit les résultats Gold et les expose via une API.</li>
        <li>Ce <span className="text-text-main font-bold">dashboard</span> interroge l&apos;API toutes les 30 secondes et rafraîchit les chiffres tout seul.</li>
      </ol>
    </div>
  </motion.div>
);

const VIEW_DATA: Record<Exclude<ViewKey, 'global-pulse' | 'help'>, { title: string; subtitle: string; icon: LucideIcon; items: PlaceholderItem[] }> = {
  'data-sources': {
    title: 'Data Sources',
    subtitle: 'Connected ingestion endpoints',
    icon: Database,
    items: [
      { name: 'GH Archive', status: 'active', detail: 'Hourly GitHub event dumps — JSON.gz over HTTPS.' },
      { name: 'DuckDB Cache', status: 'active', detail: 'Local analytical cache pre-loaded at API startup.' },
      { name: 'Bronze Lake', status: 'active', detail: 'Raw streaming layer written by Spark Structured Streaming.' },
      { name: 'Silver/Gold', status: 'idle', detail: 'Daily batch aggregation orchestrated by Airflow.' },
    ],
  },
  'kafka-streams': {
    title: 'Kafka Streams',
    subtitle: 'Topics and consumer groups',
    icon: Zap,
    items: [
      { name: 'gh-events-raw', status: 'active', detail: 'Source topic — ingestion from GH Archive producer.' },
      { name: 'gh-events-normalized', status: 'active', detail: 'Normalized stream consumed by Spark Bronze writer.' },
      { name: 'consumer: spark-bronze', status: 'active', detail: 'Lag < 200 ms — healthy.' },
      { name: 'consumer: backend-cache', status: 'idle', detail: 'Reserved for live dashboard push (WS coming).' },
    ],
  },
  'spark-jobs': {
    title: 'Spark Jobs',
    subtitle: 'Streaming and batch pipelines',
    icon: Activity,
    items: [
      { name: 'bronze-streaming-writer', status: 'active', detail: 'Structured Streaming job — Kafka → Parquet bronze.' },
      { name: 'silver-daily-rollup', status: 'idle', detail: 'Triggered by Airflow DAG gh_archive_batch.' },
      { name: 'gold-metrics-builder', status: 'idle', detail: 'Aggregates influence scores and top repos.' },
      { name: 'spark-history-server', status: 'active', detail: 'UI on port 18080 (when exposed).' },
    ],
  },
};

// --- Main Page ---

export default function Dashboard() {
  const [data, setData] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [currentView, setCurrentView] = useState<ViewKey>('global-pulse');
  const [theme, setTheme] = useState<'dark' | 'light'>('dark');

  useEffect(() => {
    document.body.classList.toggle('theme-light', theme === 'light');
  }, [theme]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
        const response = await fetch(`${apiUrl}/api/analytics/`);
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        setData(result);
        setLoading(false);
      } catch (err) {
        console.error('Error fetching analytics data:', err);
        setData({
          total_events: 0,
          active_users: 0,
          top_repos: [],
          activity_over_time: [],
          influence_scores: [],
          data_coverage: 'GitHub Archive · 15 janvier 2025 · 10h–13h UTC'
        });
        setLoading(false);
      }
    };
    fetchData();
    
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex h-screen bg-bg-deep text-text-main overflow-hidden">
      
      {/* Sidebar Cinématique */}
      <aside className="w-64 border-r border-border-subtle p-6 flex flex-col justify-between hidden lg:flex">
        <div>
          <div className="flex items-center space-x-3 mb-12">
            <div className="w-10 h-10 rounded-xl bg-primary-gold flex items-center justify-center shadow-[0_0_20px_rgba(197,160,89,0.3)]">
              <Terminal className="text-bg-deep" size={24} />
            </div>
            <h1 className="text-xl font-bold font-heading tracking-tight">PULSE<span className="text-primary-gold">.</span></h1>
          </div>

          <nav className="space-y-2">
            <p className="text-[10px] font-bold text-text-dim uppercase tracking-widest mb-4 ml-3">Navigation</p>
            <SidebarItem icon={LayoutDashboard} label="Global Pulse" active={currentView === 'global-pulse'} onClick={() => setCurrentView('global-pulse')} />
            <SidebarItem icon={Database} label="Data Sources" active={currentView === 'data-sources'} onClick={() => setCurrentView('data-sources')} />
            <SidebarItem icon={Zap} label="Kafka Streams" active={currentView === 'kafka-streams'} onClick={() => setCurrentView('kafka-streams')} />
            <SidebarItem icon={Activity} label="Spark Jobs" active={currentView === 'spark-jobs'} onClick={() => setCurrentView('spark-jobs')} />
            <SidebarItem icon={HelpCircle} label="Comment lire ?" active={currentView === 'help'} onClick={() => setCurrentView('help')} />
          </nav>
        </div>

        <div className="space-y-4">
          <PipelineStatusPanel />
          <SidebarItem icon={Settings} label="Project Settings" />
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto p-4 md:p-8 relative">
        
        {/* Header Navigation */}
        <header className="flex justify-between items-center mb-10 animate-fade" style={{ animationDelay: '0.1s' }}>
          <div>
            <h2 className="text-2xl font-bold font-heading">
              {currentView === 'global-pulse'
                ? 'Digital Instrument Dashboard'
                : currentView === 'help'
                  ? 'Comment lire ce dashboard'
                  : VIEW_DATA[currentView].title}
            </h2>
            <p className="text-text-dim text-sm">
              {currentView === 'global-pulse'
                ? 'Real-time GitHub Archive Signal Analytics'
                : currentView === 'help'
                  ? 'Guide pédagogique pour les non-techniques'
                  : VIEW_DATA[currentView].subtitle}
            </p>
            {data?.data_coverage && (
              <p className="mt-2 inline-flex items-center gap-1.5 text-xs text-text-dim bg-bg-surface border border-border-subtle rounded-full px-3 py-1">
                📅 Données analysées : {data.data_coverage}
              </p>
            )}
          </div>
          <div className="flex items-center space-x-4">
            <div className="hidden md:flex items-center bg-bg-surface border border-border-subtle rounded-full px-4 py-2 w-64 focus-within:border-primary-gold transition-colors">
              <Search size={16} className="text-text-dim" />
              <input type="text" placeholder="Search signals..." className="bg-transparent border-none focus:outline-none text-xs ml-2 w-full text-text-main" />
            </div>
            <button
              onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
              aria-label="Toggle theme"
              className="relative p-2 rounded-full border border-border-subtle hover:bg-white/5 cursor-pointer transition-colors"
            >
              {theme === 'dark' ? <Sun size={20} className="text-primary-gold" /> : <Moon size={20} className="text-text-dim" />}
            </button>
            <div className="relative p-2 rounded-full border border-border-subtle hover:bg-white/5 cursor-pointer">
              <Bell size={20} className="text-text-dim" />
              <div className="absolute top-2 right-2 w-2 h-2 bg-primary-gold rounded-full border-2 border-bg-deep" />
            </div>
            <div className="w-10 h-10 rounded-full border border-primary-gold/50 p-0.5">
              <div className="w-full h-full rounded-full bg-primary-gold flex items-center justify-center font-bold text-bg-deep">SD</div>
            </div>
          </div>
        </header>

        {currentView === 'help' && <HelpView />}

        {currentView !== 'global-pulse' && currentView !== 'help' && (
          <PlaceholderView {...VIEW_DATA[currentView]} />
        )}

        {currentView === 'global-pulse' && (<>
        {/* KPI Row */}
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6 mb-8">
          <StatCard title="Active Developers" value={loading ? "..." : data?.active_users.toLocaleString()} change="+12.5%" icon={Users} delay={0.2} />
          <StatCard title="Signal Volume" value={loading ? "..." : data?.total_events.toLocaleString()} change="+24.1%" icon={TrendingUp} delay={0.3} />
          <StatCard title="Throughput" value="1.2k/s" change="+5.2%" icon={Zap} delay={0.4} />
          <StatCard title="Data Layers" value="Bronze" change="Streaming" icon={Package} delay={0.5} />
        </div>

        {/* Charts Section */}
        <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
          
          {/* Main Activity Chart */}
          <motion.div 
            initial={{ opacity: 0, scale: 0.98 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.6, duration: 0.8 }}
            className="xl:col-span-2 glass p-8"
          >
            <div className="flex justify-between items-center mb-8">
              <div>
                <h3 className="text-lg font-bold font-heading">Global Activity Trends</h3>
                <p className="text-text-dim text-xs">Hourly commit vs pull request frequency</p>
              </div>
              <div className="flex space-x-2">
                <div className="flex items-center space-x-1.5"><div className="w-2 h-2 rounded-full bg-primary-gold" /><span className="text-[10px] text-text-dim uppercase font-bold tracking-tighter">Commits</span></div>
                <div className="flex items-center space-x-1.5"><div className="w-2 h-2 rounded-full bg-accent-emerald-bright" /><span className="text-[10px] text-text-dim uppercase font-bold tracking-tighter">PRs</span></div>
              </div>
            </div>
            
            <div className="h-[300px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={data?.activity_over_time}>
                  <defs>
                    <linearGradient id="colorCommits" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#c5a059" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#c5a059" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.02)" vertical={false} />
                  <XAxis dataKey="time" axisLine={false} tickLine={false} tick={{fill: '#71717a', fontSize: 10}} dy={10} />
                  <YAxis axisLine={false} tickLine={false} tick={{fill: '#71717a', fontSize: 10}} />
                  <Tooltip 
                    contentStyle={{ backgroundColor: '#1c1c21', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '12px' }}
                    itemStyle={{ fontSize: '12px', color: '#e4e4e7' }}
                  />
                  <Area type="monotone" dataKey="commits" stroke="#c5a059" strokeWidth={3} fillOpacity={1} fill="url(#colorCommits)" />
                  <Area type="monotone" dataKey="prs" stroke="#4caf50" strokeWidth={2} strokeDasharray="5 5" fill="transparent" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </motion.div>

          {/* Influence Distribution */}
          <motion.div 
            initial={{ opacity: 0, scale: 0.98 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.7, duration: 0.8 }}
            className="glass p-8"
          >
            <h3 className="text-lg font-bold font-heading mb-1">Ecosystem Influence</h3>
            <p className="text-text-dim text-xs mb-8">Language distribution across signals</p>
            
            <div className="h-[250px] relative">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={data?.influence_scores}
                    cx="50%" cy="50%"
                    innerRadius={60}
                    outerRadius={80}
                    paddingAngle={8}
                    dataKey="value"
                  >
                    <Cell fill="#c5a059" />
                    <Cell fill="#2e4036" />
                    <Cell fill="#1c1c21" stroke="rgba(255,255,255,0.1)" />
                    <Cell fill="#71717a" />
                  </Pie>
                </PieChart>
              </ResponsiveContainer>
              <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                <div className="text-center">
                  <p className="text-text-dim text-[10px] uppercase font-bold tracking-tighter">Leading</p>
                  <p className="text-lg font-bold text-primary-gold">JS</p>
                </div>
              </div>
            </div>

            <div className="space-y-3 mt-6">
              {data?.influence_scores.map((item, idx) => (
                <div key={idx} className="flex justify-between items-center group">
                  <div className="flex items-center space-x-2">
                    <div className="w-1.5 h-1.5 rounded-full" style={{ backgroundColor: idx === 0 ? '#c5a059' : idx === 1 ? '#4caf50' : '#71717a' }} />
                    <span className="text-xs text-text-muted group-hover:text-text-main transition-colors">{item.name}</span>
                  </div>
                  <span className="text-xs font-mono font-medium text-text-dim">{item.value}%</span>
                </div>
              ))}
            </div>
          </motion.div>

        </div>

        {/* Table / Top Repos */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8, duration: 0.8 }}
          className="mt-8 glass p-8 overflow-hidden"
        >
          <div className="flex justify-between items-center mb-8">
            <h3 className="text-lg font-bold font-heading">Trending Architectural Units</h3>
            <button className="text-xs text-primary-gold font-bold hover:underline flex items-center">View Full Repository Insights <ChevronRight size={14} /></button>
          </div>
          
          <div className="space-y-4">
            {data?.top_repos.map((repo, idx) => (
              <div key={idx} className="flex items-center justify-between p-4 rounded-2xl hover:bg-white/5 transition-all duration-300 border border-transparent hover:border-border-subtle group">
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 rounded-xl bg-bg-surface border border-border-subtle flex items-center justify-center font-bold text-text-dim group-hover:text-primary-gold transition-colors">
                    {idx + 1}
                  </div>
                  <div>
                    <p className="text-sm font-bold text-text-main">{repo.name}</p>
                    <p className="text-[10px] text-text-dim uppercase tracking-tighter">Signal Intensity: High</p>
                  </div>
                </div>
                <div className="flex items-center space-x-8">
                  <div className="hidden md:block">
                    <p className="text-xs text-text-dim mb-1 text-right">Growth</p>
                    <div className="w-24 h-1 bg-bg-surface rounded-full overflow-hidden">
                      <div className="h-full bg-primary-gold rounded-full" style={{ width: `${80 - idx * 15}%` }} />
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-mono text-text-main">{repo.activity}</p>
                    <p className="text-[10px] text-accent-emerald-bright font-bold">ACTIVE</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </motion.div>
        </>)}

        {/* Ambient background blur */}
        <div className="fixed top-[-10%] right-[-10%] w-[40%] h-[40%] bg-primary-gold opacity-[0.03] blur-[120px] rounded-full pointer-events-none" />
        <div className="fixed bottom-[-10%] left-[-10%] w-[30%] h-[30%] bg-accent-emerald-bright opacity-[0.02] blur-[100px] rounded-full pointer-events-none" />

      </main>
    </div>
  );
}
