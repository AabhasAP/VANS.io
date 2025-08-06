import { Container, Heading, Input, Button, VStack, Text } from "@chakra-ui/react";
import { useState } from "react";
import axios from "axios";

function App() {
  const [domain, setDomain] = useState("");
  const [result, setResult] = useState(null);

  const scanSubdomains = async () => {
    try {
      const res = await axios.get(`http://localhost:8000/scan/subdomains?domain=${domain}`);
      setResult(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <Container centerContent>
      <Heading my={4}>🛡 VANS - Vulnerability Scanner</Heading>
      <VStack spacing={4}>
        <Input
          placeholder="Enter domain"
          value={domain}
          onChange={(e) => setDomain(e.target.value)}
        />
        <Button colorScheme="teal" onClick={scanSubdomains}>
          Scan Subdomains
        </Button>
        {result && <Text whiteSpace="pre-wrap">{JSON.stringify(result, null, 2)}</Text>}
      </VStack>
    </Container>
  );
}

export default App;
