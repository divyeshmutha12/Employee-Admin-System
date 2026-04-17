import { useState } from "react";
import { Divider, Layout, Typography } from "antd";
import AddEmployee from "./components/AddEmployee";
import EmployeeList from "./components/EmployeeList";

const { Content, Header } = Layout;
const { Title } = Typography;

export default function App() {
  // refreshKey is a simple counter. When we increment it, EmployeeList's
  // useEffect sees a new value and re-fetches the data from the API.
  const [refreshKey, setRefreshKey] = useState(0);

  function handleEmployeeAdded() {
    // Incrementing the key tells EmployeeList to reload.
    setRefreshKey((prev) => prev + 1);
  }

  return (
    <Layout style={{ minHeight: "100vh" }}>
      <Header style={{ display: "flex", alignItems: "center" }}>
        <Title level={3} style={{ color: "white", margin: 0 }}>
          Employee Management System
        </Title>
      </Header>

      <Content style={{ padding: "32px 48px", maxWidth: 720, margin: "0 auto", width: "100%" }}>

        {/* Form to add a new employee */}
        <AddEmployee onSuccess={handleEmployeeAdded} />

        <Divider />

        {/* List of all employees — refreshes when refreshKey changes */}
        <EmployeeList refresh={refreshKey} />

      </Content>
    </Layout>
  );
}
