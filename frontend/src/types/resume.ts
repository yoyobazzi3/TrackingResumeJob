export interface ResumeListItem {
  id: string;
  is_frozen: boolean;
}

export interface Resume {
  id: string;
  content: Record<string, any>;
  is_frozen: boolean;
}
