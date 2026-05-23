import type { NextConfig } from "next";

// Ce dashboard est un sous-dossier d'un repo qui contient un autre
// package-lock.json à la racine (le site Quartz). Sans pin explicite,
// Next 16 infère ce dossier racine comme "workspace root", ce qui fausse
// le file-tracing de la sortie sur Vercel → routes introuvables → 404,
// alors même que le build est marqué "Ready".
//
// On épingle donc la racine sur le dossier du dashboard. Pendant `next build`
// (en local comme sur Vercel, où le Root Directory est ce dossier),
// process.cwd() vaut exactement ce répertoire — robuste et sans __dirname.
const projectRoot = process.cwd();

const nextConfig: NextConfig = {
  turbopack: {
    root: projectRoot,
  },
  outputFileTracingRoot: projectRoot,
};

export default nextConfig;
