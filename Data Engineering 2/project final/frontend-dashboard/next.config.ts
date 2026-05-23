import type { NextConfig } from "next";

// Le dashboard n'a aucune fonctionnalité serveur (pas de route API, pas de
// SSR dynamique) : il fetch ses données côté navigateur. On l'exporte donc
// en site 100 % statique -> dossier `out/`, servi tel quel par Cloudflare
// Pages (aucun adaptateur nécessaire).
//
// turbopack.root : ce dossier est un sous-dossier d'un repo qui a un autre
// package-lock.json à la racine (site Quartz) ; on épingle la racine ici
// pour éviter la mauvaise détection du "workspace root" pendant le build.
const projectRoot = process.cwd();

const nextConfig: NextConfig = {
  output: "export",
  images: {
    unoptimized: true,
  },
  turbopack: {
    root: projectRoot,
  },
};

export default nextConfig;
