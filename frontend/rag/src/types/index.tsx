export interface User {
  id: number;
  name: string;
  email: string;
  role: string;
}

export interface Thread {
  id: number;
  title: string;
}

export interface Message {
  id: number;
  thread_id: number;
  message: string;
  role: string;
}