import { BuildTransparency } from "@/components/build-transparency/BuildTransparency";

export default function Home() {
  return (
    <main>
      <section
        id="hero"
        className="flex min-h-[70vh] items-center px-8 md:px-16"
        style={{ backgroundColor: "var(--bg-primary)" }}
      >
        <div>
          <p
            className="mb-4 text-xs uppercase tracking-widest"
            style={{ color: "var(--muted)", fontFamily: "var(--font-mono)" }}
          >
            01 — Hero
          </p>
          <h1
            className="font-bold leading-none tracking-tight"
            style={{ fontSize: "clamp(48px, 10vw, 120px)", color: "var(--accent)" }}
          >
            PM
          </h1>
          <p className="mt-4 text-lg" style={{ color: "var(--muted)", fontFamily: "var(--font-mono)" }}>
            Sharad Rohra — Product Manager
          </p>
        </div>
      </section>

      <section
        id="contact"
        className="px-8 py-32 md:px-16"
        style={{ backgroundColor: "var(--bg-dark)" }}
      >
        <p
          className="mb-8 text-xs uppercase tracking-widest"
          style={{ color: "var(--muted)", fontFamily: "var(--font-mono)" }}
        >
          04 — Contact
        </p>
        <h2
          className="mb-12 font-light"
          style={{
            fontSize: "clamp(40px, 8vw, 96px)",
            color: "var(--text-inverse)",
            lineHeight: 1.05,
          }}
        >
          Let&apos;s talk.
        </h2>
        <a
          href="mailto:rohrasharad@gmail.com"
          className="inline-flex items-center gap-3 rounded-full border px-8 py-5 transition-colors hover:border-[#E8351A] hover:text-[#E8351A]"
          style={{
            borderColor: "rgba(255,255,255,0.2)",
            color: "var(--text-inverse)",
            fontFamily: "var(--font-mono)",
            fontSize: 15,
          }}
        >
          rohrasharad@gmail.com
        </a>
      </section>

      <BuildTransparency />
    </main>
  );
}
