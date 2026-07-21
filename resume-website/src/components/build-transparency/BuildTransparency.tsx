"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { BUILD_STATS, OPENSPEC_CAPABILITIES } from "@/lib/build-stats";
import { WorkflowDiagram } from "./WorkflowDiagram";

export function BuildTransparency() {
  const sentinelRef = useRef<HTMLDivElement>(null);
  const [visible, setVisible] = useState(false);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const el = sentinelRef.current;
    if (!el) return;

    const observer = new IntersectionObserver(
      ([entry]) => setVisible(entry.isIntersecting),
      { threshold: 0.6 },
    );
    observer.observe(el);
    return () => observer.disconnect();
  }, []);

  const close = useCallback(() => setOpen(false), []);

  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") close();
    };
    document.addEventListener("keydown", onKey);
    document.body.style.overflow = "hidden";
    return () => {
      document.removeEventListener("keydown", onKey);
      document.body.style.overflow = "";
    };
  }, [open, close]);

  return (
    <>
      <div ref={sentinelRef} className="h-px w-full" aria-hidden />

      <div
        className="border-t px-8 py-10 text-center transition-all duration-500 md:px-16"
        style={{
          borderColor: "rgba(26,26,26,0.1)",
          opacity: visible ? 1 : 0,
          transform: visible ? "translateY(0)" : "translateY(12px)",
          pointerEvents: visible ? "auto" : "none",
        }}
      >
        <p
          className="mb-4 text-[10px] uppercase tracking-[0.14em]"
          style={{ color: "var(--muted)", fontFamily: "var(--font-mono)" }}
        >
          End of page
        </p>
        <button
          type="button"
          onClick={() => setOpen(true)}
          aria-expanded={open}
          className="inline-flex items-center gap-2.5 rounded-lg border px-5 py-3 transition-colors hover:bg-black/[0.04]"
          style={{
            borderColor: "rgba(26,26,26,0.25)",
            fontFamily: "var(--font-mono)",
            fontSize: 12,
            letterSpacing: "0.03em",
            color: "var(--text-primary)",
          }}
        >
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden>
            <rect x="1" y="2" width="14" height="12" rx="2" stroke="currentColor" strokeWidth="1.2" />
            <path d="M4 6h8M4 9h5" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" />
          </svg>
          How this site was built
        </button>
      </div>

      {open && (
        <div
          className="fixed inset-0 z-[140] bg-black/50"
          onClick={close}
          aria-hidden
        />
      )}

      <div
        role="dialog"
        aria-modal={open}
        aria-labelledby="build-sheet-title"
        aria-hidden={!open}
        className={`fixed inset-x-0 bottom-0 z-[150] flex max-h-[92vh] flex-col rounded-t-[20px] transition-transform duration-300 ease-out md:inset-x-auto md:left-1/2 md:max-h-[88vh] md:w-[min(560px,calc(100%-48px))] md:-translate-x-1/2 md:rounded-2xl ${
          open ? "translate-y-0" : "translate-y-full md:translate-y-[calc(100%+2rem)]"
        }`}
        style={{
          backgroundColor: "var(--bg-dark)",
          color: "var(--text-inverse)",
        }}
      >
        <div
          className="flex items-start justify-between border-b px-6 py-5"
          style={{ borderColor: "rgba(245,237,224,0.08)" }}
        >
          <div>
            <h2 id="build-sheet-title" className="text-lg font-bold tracking-tight">
              This site auto-improves
            </h2>
            <p className="mt-1.5 max-w-sm text-[13px] leading-relaxed" style={{ color: "var(--muted)" }}>
              A closed loop — cron agents find gaps, specs get approved, agents ship previews, you approve. The portfolio literally runs on this.
            </p>
          </div>
          <button
            type="button"
            onClick={close}
            aria-label="Close"
            className="rounded-lg px-2 py-1 text-xl leading-none"
            style={{ backgroundColor: "rgba(245,237,224,0.08)" }}
          >
            ×
          </button>
        </div>

        <div className="overflow-y-auto px-6 py-5">
          <p
            className="mb-3 text-[10px] uppercase tracking-[0.14em]"
            style={{ color: "var(--accent-warm)", fontFamily: "var(--font-mono)" }}
          >
            The continuous loop
          </p>
          <WorkflowDiagram />

          <p
            className="mb-3 mt-6 text-[10px] uppercase tracking-[0.14em]"
            style={{ color: "var(--accent-warm)", fontFamily: "var(--font-mono)" }}
          >
            Current numbers
          </p>
          <div className="grid grid-cols-3 gap-2.5">
            {[
              { num: BUILD_STATS.issuesShipped, lbl: "issues shipped" },
              { num: BUILD_STATS.specToPreview, lbl: "spec → preview" },
              { num: String(BUILD_STATS.capabilities), lbl: "specced capabilities" },
            ].map((s) => (
              <div
                key={s.lbl}
                className="rounded-[10px] border px-2 py-3.5 text-center"
                style={{
                  backgroundColor: "rgba(245,237,224,0.05)",
                  borderColor: "rgba(245,237,224,0.1)",
                }}
              >
                <div className="text-[22px] font-extrabold tabular-nums" style={{ color: "var(--accent)" }}>
                  {s.num}
                </div>
                <div
                  className="mt-1.5 text-[10px] leading-snug"
                  style={{ color: "var(--muted)", fontFamily: "var(--font-mono)" }}
                >
                  {s.lbl}
                </div>
              </div>
            ))}
          </div>

          <p
            className="mb-3 mt-6 text-[10px] uppercase tracking-[0.14em]"
            style={{ color: "var(--accent-warm)", fontFamily: "var(--font-mono)" }}
          >
            OpenSpec drives the codebase
          </p>
          <div className="grid grid-cols-2 gap-1.5 md:grid-cols-3">
            {OPENSPEC_CAPABILITIES.map((cap) => (
              <span
                key={cap}
                className="text-[11px]"
                style={{ color: "var(--muted)", fontFamily: "var(--font-mono)" }}
              >
                <span style={{ color: "var(--accent-warm)" }}>— </span>
                {cap}
              </span>
            ))}
          </div>

          <p
            className="mt-5 border-t pt-4 text-[11px] leading-relaxed"
            style={{
              borderColor: "rgba(245,237,224,0.08)",
              color: "var(--muted)",
              fontFamily: "var(--font-mono)",
            }}
          >
            Stats from Linear + git. Capability list mirrors openspec/specs/. This panel is the proof — not marketing copy.
          </p>
        </div>
      </div>
    </>
  );
}
