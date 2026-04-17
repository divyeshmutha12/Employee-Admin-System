import { useEffect, useState } from "react";
import axios from "axios";
import { Alert, Button, List, Spin, Typography } from "antd";

const { Title, Text } = Typography;

export default function EmployeeList({ refresh }) {
  // ------------------------------------------------------------------
  // State variables
  // employees   : the list of employees fetched from the API
  // loading     : true while the GET request is in progress
  // error       : stores an error message if the GET request fails
  // deletingId  : the id of the employee currently being deleted
  //               (used to show a loading state on that row's button)
  // ------------------------------------------------------------------
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [deletingId, setDeletingId] = useState(null);

  // useEffect runs the fetch whenever the component mounts OR whenever
  // the parent signals a refresh (e.g. after adding a new employee).
  useEffect(() => {
    fetchEmployees();
  }, [refresh]);

  async function fetchEmployees() {
    setLoading(true); // Show spinner
    setError(null);   // Clear any previous error

    try {
      // GET /employees  →  FastAPI returns an array of employee objects
      const response = await axios.get("/employees");
      setEmployees(response.data); // Store the list in state
    } catch (err) {
      // If something goes wrong, show a friendly error message
      setError("Could not load employees. Is the backend running?");
    } finally {
      setLoading(false); // Always hide the spinner when done
    }
  }

  async function handleDelete(employeeId) {
    // Mark this specific row as deleting so its button shows a spinner.
    setDeletingId(employeeId);

    try {
      // DELETE /employees/{id}  →  FastAPI deletes the row and returns a message
      await axios.delete(`/employees/${employeeId}`);

      // Remove the deleted employee from local state immediately —
      // no need to re-fetch the whole list from the server.
      setEmployees((prev) => prev.filter((emp) => emp.id !== employeeId));
    } catch (err) {
      setError("Could not delete employee. Please try again.");
    } finally {
      setDeletingId(null); // Clear the deleting state
    }
  }

  // Show a spinner while loading
  if (loading) {
    return <Spin tip="Loading employees..." style={{ display: "block", marginTop: 40 }} />;
  }

  // Show an error alert if the request failed
  if (error) {
    return <Alert message={error} type="error" showIcon style={{ marginTop: 20 }} />;
  }

  return (
    <div>
      <Title level={4}>All Employees</Title>

      {/* Show a message when there are no employees yet */}
      {employees.length === 0 ? (
        <Text type="secondary">No employees found. Add one above!</Text>
      ) : (
        <List
          bordered
          dataSource={employees}
          renderItem={(employee) => (
            <List.Item
              key={employee.id}
              // actions renders buttons on the right side of each row
              actions={[
                <Button
                  danger
                  size="small"
                  loading={deletingId === employee.id}
                  onClick={() => handleDelete(employee.id)}
                >
                  Delete
                </Button>,
              ]}
            >
              {/* Show each employee's name and role */}
              <Text strong>{employee.name}</Text>
              <Text type="secondary" style={{ marginLeft: 12 }}>
                {employee.role}
              </Text>
            </List.Item>
          )}
        />
      )}
    </div>
  );
}
