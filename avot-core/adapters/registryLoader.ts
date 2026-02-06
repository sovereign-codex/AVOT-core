import fs from "fs";
import yaml from "js-yaml";

export class RegistryReadError extends Error {}

export class RegistryLoader {
  private registryPath: string;

  constructor(registryPath: string) {
    this.registryPath = registryPath;

    if (!fs.existsSync(this.registryPath)) {
      throw new RegistryReadError(
        `Registry file not found at ${this.registryPath}`
      );
    }
  }

  loadRegistry(): Record<string, unknown> {
    try {
      const raw = fs.readFileSync(this.registryPath, "utf-8");
      return (yaml.load(raw) as Record<string, unknown>) || {};
    } catch (err) {
      throw new RegistryReadError(
        `Failed to read registry: ${(err as Error).message}`
      );
    }
  }

  getAvotEntry(avotId: string): Record<string, unknown> {
    const registry = this.loadRegistry();
    const avots =
      (registry as any)?.avot_registry?.avots ?? {};

    return { ...(avots[avotId] || {}) };
  }

  registryMetadata(): Record<string, unknown> {
    const registry = this.loadRegistry();
    const meta = { ...(registry as any)?.avot_registry };
    delete meta.avots;
    return meta;
  }
}
