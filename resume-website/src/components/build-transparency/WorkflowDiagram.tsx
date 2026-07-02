import {
  CursorLogo,
  GitHubLogo,
  LinearLogo,
  OpenSpecLogo,
  VercelLogo,
} from "./SystemLogos";

const NODES = [
  {
    id: "feed",
    label: "Idea feeders",
    hint: "Spec-drift & bug crons",
    logo: LinearLogo,
    angle: -90,
  },
  {
    id: "spec",
    label: "Spec locked",
    hint: "agent-ready label",
    logo: LinearLogo,
    angle: -30,
  },
  {
    id: "build",
    label: "Agent builds",
    hint: "OpenSpec → code",
    logo: CursorLogo,
    angle: 30,
  },
  {
    id: "pr",
    label: "PR opened",
    hint: "GitHub branch",
    logo: GitHubLogo,
    angle: 90,
  },
  {
    id: "preview",
    label: "Preview",
    hint: "Vercel deploy",
    logo: VercelLogo,
    angle: 150,
  },
  {
    id: "live",
    label: "Approved → live",
    hint: "Spec archived",
    logo: OpenSpecLogo,
    angle: 210,
  },
] as const;

function polarToXY(angleDeg: number, radius: number, cx: number, cy: number) {
  const rad = (angleDeg * Math.PI) / 180;
  return {
    x: cx + radius * Math.cos(rad),
    y: cy + radius * Math.sin(rad),
  };
}

export function WorkflowDiagram() {
  const cx = 160;
  const cy = 160;
  const radius = 118;
  const nodeRadius = 44;

  return (
    <div className="overflow-x-auto">
      <svg
        viewBox="0 0 320 320"
        className="mx-auto w-full max-w-[320px]"
        role="img"
        aria-label="Circular auto-improve loop: idea feeders through spec, build, preview, and live deployment"
      >
        <defs>
          <marker id="loop-arrow" markerWidth="8" markerHeight="8" refX="6" refY="4" orient="auto">
            <path d="M0,0 L8,4 L0,8 Z" fill="#8A8A8A" />
          </marker>
        </defs>

        {/* Outer loop ring */}
        <circle
          cx={cx}
          cy={cy}
          r={radius}
          fill="none"
          stroke="rgba(245,237,224,0.12)"
          strokeWidth="1.5"
          strokeDasharray="6 4"
        />

        {/* Directional arc segments between nodes */}
        {NODES.map((node, i) => {
          const next = NODES[(i + 1) % NODES.length];
          const from = polarToXY(node.angle + 18, radius, cx, cy);
          const to = polarToXY(next.angle - 18, radius, cx, cy);
          return (
            <path
              key={`arc-${node.id}`}
              d={`M ${from.x} ${from.y} A ${radius} ${radius} 0 0 1 ${to.x} ${to.y}`}
              fill="none"
              stroke="rgba(232,53,26,0.45)"
              strokeWidth="1.5"
              markerEnd="url(#loop-arrow)"
            />
          );
        })}

        {/* Center label */}
        <circle cx={cx} cy={cy} r="52" fill="rgba(232,53,26,0.08)" stroke="rgba(232,53,26,0.25)" />
        <text
          x={cx}
          y={cy - 6}
          textAnchor="middle"
          fill="#F5EDE0"
          fontSize="11"
          fontWeight="600"
          fontFamily="var(--font-sans)"
        >
          Auto-improve
        </text>
        <text
          x={cx}
          y={cy + 10}
          textAnchor="middle"
          fill="#8A8A8A"
          fontSize="9"
          fontFamily="var(--font-mono)"
        >
          never stops
        </text>

        {/* Nodes */}
        {NODES.map((node) => {
          const { x, y } = polarToXY(node.angle, radius, cx, cy);
          const Logo = node.logo;
          return (
            <g key={node.id}>
              <circle
                cx={x}
                cy={y}
                r={nodeRadius}
                fill="#1A1A1A"
                stroke="rgba(245,237,224,0.15)"
                strokeWidth="1"
              />
              <foreignObject x={x - 12} y={y - 22} width="24" height="24">
                <div className="flex items-center justify-center text-[#F5EDE0]">
                  <Logo size={18} />
                </div>
              </foreignObject>
              <text
                x={x}
                y={y + 6}
                textAnchor="middle"
                fill="#F5EDE0"
                fontSize="8.5"
                fontWeight="600"
                fontFamily="var(--font-sans)"
              >
                {node.label}
              </text>
              <text
                x={x}
                y={y + 18}
                textAnchor="middle"
                fill="#8A8A8A"
                fontSize="7"
                fontFamily="var(--font-mono)"
              >
                {node.hint}
              </text>
            </g>
          );
        })}

        {/* Return arrow label — loop closes back to feeders */}
        <text
          x={cx}
          y={cy + radius + 28}
          textAnchor="middle"
          fill="#FF8C52"
          fontSize="9"
          fontFamily="var(--font-mono)"
          letterSpacing="0.06em"
        >
          live site → new gaps found → loop repeats
        </text>
      </svg>
    </div>
  );
}
