export function $http(url: string, options?: any) {
  const config = useRuntimeConfig();
  const login_token = useCookie("login_token");

  const settings = {
    baseURL: config.public.CDN_HOST + "/api",
    headers: { Authorization: `Bearer ${login_token.value ?? ""}` },
    ...options,
  };

  return $fetch<{ code: number; msg: string; result: any }>(url, settings);
}

export function formatNumber(num: number, digit = 0) {
  if (num === null || num === undefined || isNaN(num)) {
    return 0;
  }
  const number = Number(num).toLocaleString("ko-KR", {
    maximumFractionDigits: digit,
  });
  return number === "-0" ? "0" : number;
}

export function formatPhone(phoneNumber: string) {
  const match = phoneNumber.match(/^(\d{3})(\d{4})(\d{4})$/);

  if (match) {
    return `${match[1]}-${match[2]}-${match[3]}`;
  } else {
    return phoneNumber;
  }
}

export function formatDate(dateStr: Date) {
  const date = new Date(dateStr);
  const year = date.getFullYear();
  // 월은 0부터 시작하므로 +1 후, 2자리 숫자로 변환합니다.
  const month = (date.getMonth() + 1).toString().padStart(2, "0");
  const day = date.getDate().toString().padStart(2, "0");
  return `${year}-${month}-${day}`;
}

export function scrollToTop() {
  window.scrollTo(0, 0);
}

// export function stringToInt(amt: any) {
// 	if (!amt) return 0;
// 	return parseFloat(String(amt).replace(/[^0-9.-]/g, ''));
// }

// export const isEmpty = (value: any): boolean => {
// 	if (!value) return true;
// 	else if (Array.isArray(value) && value.length === 0) return true;
// 	else if (typeof value === 'object' && value !== null && Object.keys(value).length === 0) return true;

// 	return false;
// };

export const isEmpty = (value: any): boolean => {
  // falsy값 chk : false, 0, "", null, undefined, NaN
  if (!value) return true;
  // 빈 배열 chk
  if (Array.isArray(value) && value.length === 0) return true;
  // 빈 객체 chk
  if (
    typeof value === "object" &&
    value !== null &&
    Object.keys(value).length === 0
  )
    return true;

  return false;
};

export function validatePhone(phone: string) {
  const phoneRegex =
    /^01(1|[6-9])(-?)(\d{3,4})(-?)(\d{4})$|^010(-?)(\d{3,4})(-?)(\d{4})$/;
  return phoneRegex.test(phone);
}

export function activate_confirm(
  model: { title: string; text: string; active: boolean },
  title: "",
  text: string
) {
  model.active = true;
  model.title = title;
  model.text = text;
}
