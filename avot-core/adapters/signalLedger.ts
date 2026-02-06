import fs from "fs";
import yaml from "js-yaml";
import { v4 as uuidv4 } from "uuid";

export class SignalLedgerError extends Error {}

export class SignalLedger {
  private ledgerPath: string;

  constructor(ledgerPath: string) {
    this.ledgerPath = ledgerPath;

    if (!fs.existsSync(this.ledgerPath)) {
      throw new SignalLedgerError(
        `Signal ledger not found at ${this.ledgerPath}`
      );
    }
  }

  private load(): any {
    try {
      const raw = fs.readFileSync(this.ledgerPath, "utf-8");
      return yaml.load(raw) || {};
    } catch (err) {
      throw new SignalLedgerError(
        `Failed to read signal ledger: ${(err as Error).message}`
      );
    }
  }

  private write(data: any): void {
    try {
      fs.writeFileSync(
        this.ledgerPath,
        yaml.dump(data, { sortKeys: false }),
        "utf-8"
      );
    } catch (err) {
      throw new SignalLedgerError(
        `Failed to write signal ledger: ${(err as Error).message}`
      );
    }
  }

  readSignals(): any[] {
    const ledger = this.load();
    return ledger?.signal_ledger?.signals ?? [];
  }

  appendSignal(
    avotId: string,
    signalType: string,
    description: string,
    severity: string = "low",
    context: Record<string, unknown> = {},
    metadata: Record<string, unknown> = {}
  ): any {
    const ledger = this.load();

    if (!ledger.signal_ledger) {
      throw new SignalLedgerError("Invalid signal ledger structure");
    }

    const signal = {
      signal_id: `SIG-${uuidv4()}`,
      avot_id: avotId,
      signal_type: signalType,
      timestamp: new Date().toISOString(),
      severity,
      description,
      context,
      metadata,
    };

    ledger.signal_ledger.signals.push(signal);
    this.write(ledger);

    return signal;
  }
}
