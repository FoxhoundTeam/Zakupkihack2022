export const isCompany = (user) => user.role === "company";
export const isAdminOrModerator = (user) =>
  ["admin", "moderator"].includes(user.role);
