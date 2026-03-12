# Issue-to-Commit Resolution Map

## Verified Closed Issues with Code Resolutions

These commands should be run in the `agent-lightning` repository directory.

| Issue | Description | Commit | Shell Command |
|-------|-------------|--------|---------------|
| #134 | trace_aggregator (transition/trajectory) | `4235731a` | `cd agent-lightning && git show 4235731a` |
| #208 | Support VERL 0.6 / vLLM 0.11 | `5f62ecb6` | `cd agent-lightning && git show 5f62ecb6` |
| #370 | ctrl+c graceful shutdown | `337cce7f` | `cd agent-lightning && git show 337cce7f` |
| #383/#386 | LoRA compatibility | `bbd5c2a3` | `cd agent-lightning && git show bbd5c2a3` |
| #394 | vLLM 0.10.2/0.11.0 split | `5f62ecb6` | `cd agent-lightning && git show 5f62ecb6` |
| #403 | TraceTree/match_rewards fix | (see below) | `cd agent-lightning && git log --oneline --all \| grep -i "match_rewards\|403"` |
| #407 | Customizable trainer/daemon | `1d199b21` | `cd agent-lightning && git show 1d199b21` |
| #443 | APO templates configurable | `bfb94a87` | `cd agent-lightning && git show bfb94a87` |
| #478 | Agent-OS integration | `49bf9cd9` | `cd agent-lightning && git show 49bf9cd9` |
| N/A | Pin verl<0.7.0 | `7690d1e8` | `cd agent-lightning && git show 7690d1e8` |
| N/A | Empty tensor/failed rollouts fix | `19c72db6` | `cd agent-lightning && git show 19c72db6` |

## Closed Issues WITHOUT Code Resolutions (Discussion Only)

| Issue | Description | Comments | Note |
|-------|-------------|----------|------|
| #67 | verl-agent vs agent-lightning | 6 comments | Architectural clarification |
| #77 | training_rollout_async no return | 1 comment | Design choice explanation |
| #104 | Multiple actors in rollout | 3 comments | Confirmed support |

Verify with: `cd agent-lightning && git log --all --oneline | grep -i "verl-agent\|training_rollout_async\|ray hang"` (should return empty)

## Open Issues — Candidates for Exercises

| Issue | Description | Exercise Mapping |
|-------|-------------|-----------------|
| #490 | Exploration collapse | **Ex.10** (§3.2.exercises): spectral test on policy trajectory |
| #489 | GRPO grouping in multi-turn | Related to §3.3.credit |
| #470 | Local models / OpenRouter | Potential exercise on NxD Inference config |
| #464 | VERL hyperparams not taking effect | Related to NEW-75 |
| #448 | Failed rollouts | §3.3.2 gap test (inter-failure interval) |
| #438 | Memory leak | §3.3.2 gap test + §3.2.migration.memory |
| #392 | Credit assignment taxonomy | **Ex.9** (§3.2.exercises): variance derivation |
| #108 | Ascend NPU support | §3.2.critical: 4th hardware platform |

## Additional Commit Searches Needed

I could not find exact commit hashes for these issues in git_log.txt.
Please run these in the agent-lightning repo to locate them:

```bash
# #109 (DeepWerewolf case study)
cd agent-lightning && git log --all --oneline | grep -i "werewolf\|deepwerewolf\|109"

# #272 (NPU support discussion)
cd agent-lightning && git log --all --oneline | grep -i "npu\|ascend\|272"

# #403 (match_rewards fix)
cd agent-lightning && git log --all --oneline | grep -i "match_rewards\|assign_to\|403"

# #112 (relates to DeepWerewolf)
cd agent-lightning && git log --all --oneline | grep -i "112"
```

Also for operatorRL:
```bash
# Check agent-lightning integration module
cd operatorRL && find . -path "*/agent_lightning/*" -name "*.py" | head -10
cd operatorRL && git log --oneline -10
```
