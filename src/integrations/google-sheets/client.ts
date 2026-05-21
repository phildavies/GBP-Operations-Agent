export interface SheetPostInput {
  businessId: string;
  postType: "event" | "offer" | "update";
  title: string;
  description?: string;
  startDate?: string;
  endDate?: string;
  cta?: string;
  imageUrl?: string;
}

export interface GoogleSheetsClient {
  readPostInputs(spreadsheetId: string, range: string): Promise<SheetPostInput[]>;
}

export class PlaceholderGoogleSheetsClient implements GoogleSheetsClient {
  async readPostInputs(
    _spreadsheetId: string,
    _range: string
  ): Promise<SheetPostInput[]> {
    throw new Error("Google Sheets integration not implemented yet.");
  }
}
