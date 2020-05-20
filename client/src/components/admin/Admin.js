import React from "react";
import "../../css/admin/Admin.css";
import Stopword from "./Stopword";

const Admin = () => {
  return (
    <div className="Admin-wrapper">
      <div className="Title">Admin</div>
      <div>
        <Stopword></Stopword>
      </div>
    </div>
  );
};

export default Admin;
