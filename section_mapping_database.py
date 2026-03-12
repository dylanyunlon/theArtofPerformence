#!/usr/bin/env python3
"""
section_mapping_database.py
Maps every substantive content block from current TheArtofAgenticSystems.tex
to the EXACT TAOCP Chapter 3 section numbering.

TAOCP Chapter 3 structure (FIXED, from images):
  3.1   Introduction
  3.2   Generating Uniform Random Numbers
    3.2.1   Linear Congruential Method
      3.2.1.1   Choice of Modulus
      3.2.1.2   Choice of Multiplier
      3.2.1.3   Potency
    3.2.2   Other Methods
  3.3   Statistical Tests
    3.3.1   General Test Methods
    3.3.2   Empirical Tests
    *3.3.3  Theoretical Tests
    3.3.4   Spectral Test
  3.4   Other Types of Random Quantities
    3.4.1   Numerical Distributions
    3.4.2   Random Sampling and Shuffling
  *3.5  What Is a Random Sequence
  3.6   Summary
"""

import json

# Each entry: (source_description, old_location, new_target, content_summary)
MAPPING = [
    # ===== §3.1-§3.2: KEEP AS-IS =====
    ("§3.1 Introduction", "L88-282", "§3.1", "KEEP: 195 lines unchanged"),
    ("§3.2 + all subsections", "L283-1001", "§3.2", "KEEP: 719 lines unchanged"),

    # ===== OLD §3.3 content → REDISTRIBUTE =====
    # §3.3.1 General Tests
    ("χ² test: NeuronCore utilization", "old §3.3.1(i)", "§3.3.1", 
     "KEEP: χ² applied to k NeuronCores, V statistic, ν=k-1 df, critical value 82.5 for k=64"),
    ("χ² test: Reward distribution", "old §3.3.1(ii)", "§3.3.1",
     "KEEP: Reward bins, exploration collapse indicator"),
    ("χ² test: Gradient norm", "old §3.3.1(iii)", "§3.3.1",
     "KEEP: Distributed training straggler detection"),
    ("χ² Table 3.3.1-1", "old §3.3.1", "§3.3.1", "KEEP: percentile table"),
    ("KS test: reward convergence", "old §3.3.1B", "§3.3.1",
     "KEEP: Two-sample KS, convergence/forgetting/staleness detection"),
    ("TAOCP χ² derivation (eq chi2-dist)", "new", "§3.3.1", 
     "ADD: Polar coordinate derivation → incomplete gamma function"),
    ("TAOCP KS exact distribution (eq ks-exact)", "new", "§3.3.1",
     "ADD: Smirnov formula, large-n approximation"),
    
    # §3.3.2 Empirical Tests
    ("Run Test → Rollout Length Stability", "old §3.3.2", "§3.3.2", "KEEP"),
    ("Gap Test → Inter-Failure Interval", "old §3.3.2", "§3.3.2", "KEEP"),
    ("Serial Test → Consecutive Action Correlation", "old §3.3.2", "§3.3.2", "KEEP"),
    ("Poker Test → Action Diversity", "old §3.3.2", "§3.3.2", "KEEP"),
    ("OOM 3-pattern case study", "old §3.3.2", "§3.3.2",
     "KEEP: trajectory accumulation, KV-cache frag, gradient buffer persistence"),
    ("trace_aggregator as Serial Test Enabler", "old §3.3.2", "§3.3.2", "KEEP"),
    
    # *§3.3.3 Theoretical Tests ← NEW SECTION (most critical gap)
    ("GRPO Temporal Correlation Theorem", "old §3.3.2", "★§3.3.3",
     "MOVE: Theorem + proof sketch → theoretical validation of batching"),
    ("CRT version compatibility analysis", "old §3.3.1C", "★§3.3.3",
     "MOVE: v_i ≡ v_i* (mod M_i) → theoretical dependency analysis"),
    ("4-layer migration map as validation theory", "old §3.3.3", "★§3.3.3",
     "REWRITE: Parallelism/Kernels/Comm/Memory → theoretical failure mode taxonomy"),
    ("Cartesian product of debug spaces", "old §3.3.3", "★§3.3.3",
     "MOVE: O(3·k·d) worst-case analysis → theoretical complexity bound"),
    ("Degenerate cross-platform configs", "old §3.3.4", "★§3.3.3",
     "MOVE: Configuration independence proof → theoretical validation limit"),
    ("Governance invariant formal proofs", "new", "★§3.3.3",
     "ADD: Formal proof that 4 kernel invariants are sufficient for crash isolation (M13,M14)"),
    
    # §3.3.4 Spectral Test (PURE spectral, nothing else)
    ("Spectral test: lattice structure", "old §3.3.4", "§3.3.4",
     "KEEP: ν_d min distance, Trainium2 GEMM 4-param auto-tuner"),
    ("Spectral test: policy parameter trajectory", "old §3.3.4", "§3.3.4",
     "KEEP: Periodic orbit detection in parameter space"),
    
    # ===== §3.4 Other Types ← ENTIRELY NEW =====
    # §3.4.1 Numerical Distributions
    ("Credit assignment: 3 strategies", "old §3.3.6", "★§3.4.1",
     "MOVE: trajectory/transition/action-level + memory implications (M5,M6,M7)"),
    ("Exploration collapse: trajectory entropy", "old §3.3.5", "★§3.4.1",
     "MOVE: H_W entropy, reward staleness, novelty-routine matrix (M5→Issue#490)"),
    ("On-policy vs off-policy distinction", "new", "★§3.4.1",
     "ADD: Fundamental RL distinction + hardware utilization impact (M11)"),
    ("LoRA/parameter-efficient distributions", "new", "★§3.4.1",
     "ADD: Fused LoRA kernel migration Trainium2 (M12→Issue#365,#383)"),
    ("Process rewards / intermediate rewards", "new", "★§3.4.1",
     "ADD: Causal credit assignment across tool-use steps (M7→Issue#387,#390,#392)"),
    ("Thinking mode / reasoning tokens", "new", "★§3.4.1",
     "ADD: CoT compute cost in rollouts, KV-cache inflation (M20→Issue#347)"),
    ("Reward formula: R_final composition", "old §3.3.3", "§3.4.1",
     "MOVE: PolicyReward additive/multiplicative formula"),
    
    # §3.4.2 Random Sampling and Shuffling
    ("Multi-agent: Nexus trust exchange", "old §3.3.5", "★§3.4.2",
     "MOVE: registry/reputation/escrow/arbiter/dmz + trust-weighted rewards (M9)"),
    ("Multi-agent: Mute Agent architecture", "old §3.3.5", "★§3.4.2",
     "MOVE: Face/Hands reasoning+execution decomposition"),
    ("Multi-agent: Hardware partitioning", "old §3.3.5", "★§3.4.2",
     "MOVE: NeuronCore partitioning, MIG comparison"),
    ("Composite modulus convergence analogy", "old §3.3.5", "★§3.4.2",
     "MOVE: lcm(λ_1,...,λ_n) multi-agent period decomposition"),
    ("Distributed rollout parallelism", "new", "★§3.4.2",
     "ADD: Why 1-of-8 GPUs used, Trainium2 solution (M15→Issue#82,#104,#106)"),
    ("Rollout timeout and failure handling", "new", "★§3.4.2",
     "ADD: Failed rollout retry strategies + hardware cost (M16→Issue#218,#448)"),
    ("Multimodal agent training", "new", "★§3.4.2",
     "ADD: Vision encoder kernel migration exercise (M10→Issue#105,#110)"),
    
    # ===== *§3.5 What Is an Agentic System ← ENTIRELY NEW =====
    ("Self-evolving loop definition", "old §3.3.3", "★§3.5",
     "MOVE: rollout→reward→update→deploy→iterate"),
    ("System architecture ASCII figure", "old §3.3.3", "★§3.5",
     "MOVE: OperatorRL/AgentLightning/HW 3-layer figure"),
    ("4 kernel invariants", "old §3.3.3", "★§3.5",
     "MOVE: No Bypass, Fail Closed, Audit Everything, Crash Isolation"),
    ("Signal dispatch table", "old §3.3.3", "★§3.5",
     "MOVE: SIGKILL/SIGEXPLORE/SIGPOLICY/SIGTRUST"),
    ("Integration bridge: 4 adapter components", "old §3.3.3", "★§3.5",
     "MOVE: GovernedRunner/PolicyReward/FlightRecorderEmitter/GovernedEnvironment"),
    ("Daemon: two execution modes", "old §3.3.3", "★§3.5",
     "MOVE: v0=HTTP server, v1=LightningStore"),
    ("CCCL ecosystem analysis", "old §3.3.3", "★§3.5",
     "MOVE: Thrust/CUB/libcudacxx → 'makes NVIDIA prison more luxurious'"),
    ("NVIDIA vs Trainium stack table", "old §3.3.3", "★§3.5",
     "MOVE: Complete stack correspondence"),
    ("Open-source counterstrategy: XLA/JAX/NKI", "old §3.3.3", "★§3.5",
     "MOVE: AWS 3-pronged approach"),
    ("SCAK module architecture", "new", "★§3.5",
     "ADD: Self-correcting kernel formal description (M13)"),
    ("Control-plane scheduling algorithm", "new", "★§3.5",
     "ADD: Formalize as Algorithm C (M14)"),
    ("Ascend NPU acknowledgment", "new", "★§3.5",
     "ADD: Fourth hardware platform (M21→Issue#108)"),
    ("Dashboard and observability", "new", "★§3.5",
     "ADD: operatorRL/modules/observability + agentlightning/dashboard (M18)"),
    
    # ===== §3.6 Summary ← NEW =====
    ("OperatorRL module reference", "old Appendix A", "§3.6",
     "MOVE+CONDENSE: Module table with §3.x cross-refs"),
    ("Agent Lightning component reference", "old Appendix B", "§3.6",
     "MOVE+CONDENSE: Component table with §3.x cross-refs"),
    ("Chapter exercises (14 problems)", "old Exercises", "§3.6",
     "MOVE: Exercises distributed per-section + collected in §3.6"),
]

def main():
    # Count by target
    targets = {}
    for desc, old, new, summary in MAPPING:
        targets.setdefault(new, []).append((desc, summary))
    
    print("=" * 70)
    print("SECTION MAPPING DATABASE")
    print("TAOCP Ch.3 exact numbering → TheArtofAgenticSystems.tex")
    print("=" * 70)
    
    for target in sorted(targets.keys()):
        entries = targets[target]
        star = "★★" if target.startswith("★") else ""
        print(f"\n{star} {target} ({len(entries)} content blocks)")
        for desc, summary in entries:
            print(f"    {desc}")
            print(f"      → {summary}")
    
    # Summary stats
    keep = sum(1 for _,_,_,s in MAPPING if s.startswith("KEEP"))
    move = sum(1 for _,_,_,s in MAPPING if s.startswith("MOVE"))
    add = sum(1 for _,_,_,s in MAPPING if s.startswith("ADD"))
    rewrite = sum(1 for _,_,_,s in MAPPING if s.startswith("REWRITE"))
    
    print(f"\n{'='*70}")
    print(f"TOTALS: {len(MAPPING)} content blocks")
    print(f"  KEEP:    {keep} (preserve in current section)")
    print(f"  MOVE:    {move} (relocate to correct TAOCP section)")
    print(f"  ADD:     {add} (new content from plan.md M-items)")
    print(f"  REWRITE: {rewrite} (restructure existing content)")
    
    with open('section_mapping.json', 'w') as f:
        json.dump([{"desc": d, "old": o, "new": n, "summary": s} 
                   for d,o,n,s in MAPPING], f, indent=2)
    print(f"\nSaved to section_mapping.json")

if __name__ == '__main__':
    main()
