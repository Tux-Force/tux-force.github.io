// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import starlightBlog from 'starlight-blog';

const github = 'https://github.com/Tux-Force';

// https://astro.build/config
export default defineConfig({
	site: 'https://tux-force.github.io',
	integrations: [
		starlight({
			title: 'Tux-Force',
			description:
				'The PC games you own or subscribe to, on Linux: real licenses, no cracks. Sign-in, downloads, runtime, Wine and launcher.',
			logo: {
				light: './src/assets/logo-light.svg',
				dark: './src/assets/logo-dark.svg',
				replacesTitle: true,
			},
			favicon: '/favicon.svg',
			head: [
				{ tag: 'link', attrs: { rel: 'icon', href: '/favicon.ico', sizes: '32x32' } },
				{ tag: 'link', attrs: { rel: 'apple-touch-icon', href: '/apple-touch-icon.png' } },
				{ tag: 'meta', attrs: { property: 'og:image', content: 'https://tux-force.github.io/social-preview.png' } },
				{ tag: 'meta', attrs: { name: 'twitter:card', content: 'summary_large_image' } },
			],
			// English only for now. German goes in as a second locale (`de`) with translated pages in `src/content/docs/de/`.
			defaultLocale: 'root',
			locales: {
				root: { label: 'English', lang: 'en' },
			},
			social: [{ icon: 'github', label: 'GitHub', href: github }],
			editLink: { baseUrl: `${github}/tux-force.github.io/edit/develop/` },
			lastUpdated: true,
			customCss: ['./src/styles/brand.css'],
			plugins: [
				starlightBlog({
					title: 'News',
					authors: {
						tuxforce: { name: 'Tux-Force', picture: '/brand/avatar-512.png', url: github },
					},
				}),
			],
			sidebar: [
				{
					label: 'Guide',
					items: [
						{ label: 'Quick start', slug: 'guide/quick-start' },
						{ label: 'Installation', slug: 'guide/installation' },
						{ label: 'Wine prefix', slug: 'guide/prefix' },
						{ label: 'Sign-in and password prompts', slug: 'guide/sign-in' },
						{ label: 'Running games', slug: 'guide/running-games' },
						{ label: 'Launcher', slug: 'guide/launcher' },
						{ label: 'Troubleshooting', slug: 'guide/troubleshooting' },
						{ label: 'FAQ', slug: 'guide/faq' },
					],
				},
				{ label: 'Compatibility', slug: 'compatibility' },
				{ label: 'Downloads', slug: 'downloads' },
				{
					label: 'Project',
					items: [
						{ label: 'Vision', slug: 'project/vision' },
						{ label: 'Roadmap', slug: 'project/roadmap' },
						{ label: 'Architecture', slug: 'project/architecture' },
						{ label: 'Launcher plan', slug: 'project/launcher-plan' },
						{ label: 'Contributing', slug: 'project/contributing' },
						{ label: 'Brand', slug: 'project/brand' },
					],
				},
			],
		}),
	],
});
