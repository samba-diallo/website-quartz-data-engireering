import { QuartzConfig } from "./quartz/cfg"
import * as Plugin from "./quartz/plugins"

/**
 * Quartz 4 Configuration
 *
 * See https://quartz.jzhao.xyz/configuration for more information.
 */

// Déterminer l'environnement
const isProduction = process.env.NODE_ENV === "production"

// Définir la base URL selon l'environnement
const getBaseUrl = (): string => {
  if (isProduction) {
    // Remplace avec ton domaine final si tu en as un
    return "website-quartz-data-engireering.pages.dev"
    // Ou si tu as un domaine personnalisé :
    // return "data-engineering.com"
  }
  return "localhost:8080"
}

const config: QuartzConfig = {
  configuration: {
    pageTitle: "Data Engineering 1",
    pageTitleSuffix: "",
    enableSPA: true,
    enablePopovers: true,
    analytics: {
      provider: "",
    },
    locale: "fr-FR",
    // ✅ URL dynamique : localhost en dev, production en prod
    baseUrl: getBaseUrl(),
    ignorePatterns: ["private", "templates", ".obsidian"],
    defaultDateType: "modified",
    theme: {
      fontOrigin: "googleFonts",
      cdnCaching: true,
      typography: {
        header: "Schibsted Grotesk",
        body: "Source Sans Pro",
        code: "IBM Plex Mono",
      },
      colors: {
        lightMode: {
          light: "#faf8f8",
          lightgray: "#e5e5e5",
          gray: "#b8b8b8",
          darkgray: "#4e4e4e",
          dark: "#2b2b2b",
          secondary: "#284b63",
          tertiary: "#84a59d",
          highlight: "rgba(143, 159, 169, 0.15)",
          textHighlight: "#fff23688",
        },
        darkMode: {
          light: "#161618",
          lightgray: "#393639",
          gray: "#646464",
          darkgray: "#d4d4d4",
          dark: "#ebebec",
          secondary: "#7b97aa",
          tertiary: "#84a59d",
          highlight: "rgba(143, 159, 169, 0.15)",
          textHighlight: "#b3aa0288",
        },
      },
    },
  },
  plugins: {
    transformers: [
      Plugin.FrontMatter(),
      Plugin.CreatedModifiedDate({
        priority: ["frontmatter", "git", "filesystem"],
      }),
      Plugin.SyntaxHighlighting({
        theme: {
          light: "github-light",
          dark: "github-dark",
        },
        keepBackground: false,
      }),
      Plugin.ObsidianFlavoredMarkdown({ enableInHtmlEmbed: false }),
      Plugin.GitHubFlavoredMarkdown(),
      Plugin.TableOfContents(),
      Plugin.CrawlLinks({ markdownLinkResolution: "relative" }),
      Plugin.Description(),
      Plugin.Latex({ renderEngine: "katex" }),
    ],
    filters: [
      Plugin.RemoveDrafts(),
    ],
    // 🔑 ORDRE CORRECT DES EMITTERS (CRITIQUE)
    emitters: [
      Plugin.AliasRedirects(),
      Plugin.ComponentResources(),
      // ✅ Assets AVANT la génération des pages
      Plugin.Assets(),
      Plugin.Static(),
      // Pages Quartz
      Plugin.ContentPage(),
      Plugin.FolderPage(),
      Plugin.TagPage(),
      Plugin.ContentIndex({
        enableSiteMap: true,
        enableRSS: true,
      }),
      Plugin.Favicon(),
      Plugin.NotFoundPage(),
      // Optionnel (lent, tu peux le laisser commenté)
      // Plugin.CustomOgImages(),
    ],
  },
}

export default config