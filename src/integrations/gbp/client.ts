export interface GbpLocationSummary {
  accountId: string;
  locationId: string;
  displayName: string;
  address?: string;
}

export interface GbpClient {
  listLocations(): Promise<GbpLocationSummary[]>;
  getLocation(locationId: string): Promise<unknown>;
  getReviews(locationId: string): Promise<unknown[]>;
  getPosts(locationId: string): Promise<unknown[]>;
  getMedia(locationId: string): Promise<unknown[]>;
}

export class PlaceholderGbpClient implements GbpClient {
  async listLocations(): Promise<GbpLocationSummary[]> {
    throw new Error("GBP integration not implemented yet.");
  }

  async getLocation(_locationId: string): Promise<unknown> {
    throw new Error("GBP integration not implemented yet.");
  }

  async getReviews(_locationId: string): Promise<unknown[]> {
    throw new Error("GBP integration not implemented yet.");
  }

  async getPosts(_locationId: string): Promise<unknown[]> {
    throw new Error("GBP integration not implemented yet.");
  }

  async getMedia(_locationId: string): Promise<unknown[]> {
    throw new Error("GBP integration not implemented yet.");
  }
}
