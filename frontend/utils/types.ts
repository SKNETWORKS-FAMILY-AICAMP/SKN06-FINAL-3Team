type RoleTypes = 3 | 2 | 1 | 0; // '시스템관리자' | '관리자' | '일반' | '';

interface ResponseOutput {
  code: number;
  detail: String;
  result: any;
  totalRows?: any;
}

interface JwtPayloadOptions {
  member_id: number;
  emp_no: string;
  company_affiliation: string;
  phone: string;
  employment_status: string;
  position: string;
  department: string;
  name: string;
  role: RoleTypes;
}

export interface MemberOptions extends JwtPayloadOptions {}
