/**
 * AVOT Interface
 * Canonical behavioral contract for all AVOT implementations.
 *
 * This interface defines WHAT an AVOT must be able to do,
 * not HOW it does it.
 *
 * No enforcement logic belongs here.
 */

export type LifecycleState =
  | "S0" | "S1" | "S2" | "S3" | "S4"
  | "S5" | "S6" | "S7" | "S8" | "S9";

export type MaturityLevel = "M0" | "M1" | "M2" | "M3" | "M4";

export type ActionType =
  | "think"
  | "communicate"
  | "execute"
  | "bind"
  | "propose";

export type RefusalReason =
  | "scope"
  | "lifecycle"
  | "consent"
  | "covenant"
  | "unknown";

export interface AvotIdentity {
  avot_id: string;
  purpose?: string;
  steward?: string;
  header_ref?: string;
}

export interface AvotState {
  lifecycle_state: LifecycleState;
  maturity: MaturityLevel;
  binding: boolean;
}

export interface AvotRefusal {
  reason: RefusalReason | string;
  reference: string;
  next_step: "wait" | "propose" | "escalate" | "dissolve";
}

export interface AvotSignal {
  avot_id: string;
  signal_type: string;
  payload: Record<string, unknown>;
  timestamp: string;
}

/**
 * Canonical AVOT behavioral interface
 */
export interface AVOT {
  /**
   * Identity awareness
   */
  identify(): AvotIdentity;

  /**
   * Lifecycle & state awareness
   */
  state(): AvotState;

  /**
   * Classify an intended behavior into an action type
   */
  classifyAction(intent: string): ActionType;

  /**
   * Evaluate whether an action type may be attempted
   */
  canAttempt(action: ActionType): boolean;

  /**
   * Produce a structured refusal
   * Refusal is a valid outcome, not an error.
   */
  refuse(
    reason: RefusalReason | string,
    reference: string,
    nextStep?: AvotRefusal["next_step"]
  ): AvotRefusal;

  /**
   * Emit a non-binding signal
   */
  emitSignal(
    signalType: string,
    payload?: Record<string, unknown>
  ): AvotSignal;
}