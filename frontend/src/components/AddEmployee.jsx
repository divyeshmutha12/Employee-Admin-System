import { useState } from "react";
import axios from "axios";
import { Alert, Button, Form, Input, Typography } from "antd";

const { Title } = Typography;

// onSuccess is a function passed from the parent.
// We call it after a successful add so the employee list refreshes.
export default function AddEmployee({ onSuccess }) {
  // ------------------------------------------------------------------
  // State variables
  // name    : the value of the name input field
  // role    : the value of the role input field
  // loading : true while the POST request is in progress
  // success : set to true when the employee is created successfully
  // error   : stores an error message if the request fails
  // ------------------------------------------------------------------
  const [name, setName] = useState("");
  const [role, setRole] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState(null);

  async function handleSubmit() {
    setSuccess(false);
    setError(null);

    // Basic validation — do not send blank values to the API
    if (!name.trim() || !role.trim()) {
      setError("Both name and role are required.");
      return;
    }

    setLoading(true);

    try {
      // POST /employees  →  sends { name, role } as JSON body
      await axios.post("/employees", { name: name.trim(), role: role.trim() });

      setSuccess(true); // Show success message
      setName("");      // Reset the name field
      setRole("");      // Reset the role field
      onSuccess();      // Tell the parent to refresh the employee list
    } catch (err) {
      setError("Failed to add employee. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ maxWidth: 480 }}>
      <Title level={4}>Add Employee</Title>

      {/* Show success message after a successful submission */}
      {success && (
        <Alert
          message="Employee added successfully!"
          type="success"
          showIcon
          closable
          style={{ marginBottom: 16 }}
        />
      )}

      {/* Show error message if something went wrong */}
      {error && (
        <Alert
          message={error}
          type="error"
          showIcon
          closable
          style={{ marginBottom: 16 }}
        />
      )}

      <Form layout="vertical" onFinish={handleSubmit}>

        {/* Name field */}
        <Form.Item label="Employee Name">
          <Input
            placeholder="e.g. John Doe"
            value={name}
            onChange={(e) => setName(e.target.value)} // Update state on every keystroke
          />
        </Form.Item>

        {/* Role field */}
        <Form.Item label="Role">
          <Input
            placeholder="e.g. Developer"
            value={role}
            onChange={(e) => setRole(e.target.value)}
          />
        </Form.Item>

        {/* Submit button — shows loading state while the request is pending */}
        <Form.Item>
          <Button type="primary" htmlType="submit" loading={loading}>
            Add Employee
          </Button>
        </Form.Item>

      </Form>
    </div>
  );
}
