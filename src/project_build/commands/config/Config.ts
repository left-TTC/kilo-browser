
export interface Config {
    schemaVersion: number;

    project: {
        name: string;
        schemaName: string;
        company: string,
    };

    brave: {
        path: string;
        version: string;
    };

    features: {
        enableLeoAi: boolean;
        enableBraveVpn: boolean;
    };
}
